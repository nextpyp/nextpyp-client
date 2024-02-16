
===============
Getting Started
===============


Installation
------------

First, install the NextPYP Client python package. There are a few different options for installation:


:strikethrough:`Installing from PyPI`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: shell

	pip install next-pyp

.. warning::

	The package hasn't been uploaded to PyPI yet, so this option won't work for now.
	See one of the other installation options below.


Installing from precompiled wheel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you already have a precompiled ``.whl`` file, install it using ``pip``:

.. code-block:: shell

	pip install path/to/nextpyp_client-version-arch.whl


Installing from source
^^^^^^^^^^^^^^^^^^^^^^

Or you can install the project directly from the source tree.
First, check out the project from git. Then install the module in development mode.

.. code-block:: shell

	pyp install -e path/to/nextpyp-client


Overview
--------

The NextPYP API is organized heirarchically. The highest level in the heirachy is a `service`.
Services come in two flavors: `regular` and `realtime`.

Regular services follow a Remote Procedure Call (RPC) model where the client calls a function, sends arguments,
and then waits for a response. Each service has a specific focus (like preprocessing, or sessions, etc) and all
the functions under that service are related to that focus.

Each regular service function also requires a specific permission to be used. For example, the hypothetical ``bar``
function in the ``foo`` regular service may require a permission named ``foo_bar``. Not all regular functions require
permissions. Some functions are left permissionless and can be accessed by unauthenticated clients, but these
permissionless functions generally only provide enough functionality to request access to permissioned functions
and not much else. The API documentation for each service function will explain what permission is needed to use it.

Realtime services differ from regular services by not having functions. Instead, realtime services work more like
a bidirectional communication channel. Once the channel is open, the client can send an outgoing message, or wait
for an incoming message. It's up to the server to decide when to send messages
to the client, so this mechanism lets the client listen for updates from the server in real-time.

Each realtime service also needs a permission to be used by a client. These permissions tend to be named
something like ``servicename_listen``. The API documentation for each realtime service will explain what permission
is needed to use it.

To use the NextPYP client, you will need to request the needed permissions from a specific user account on the
NextPYP website. Once submitted, the request will be visible on the user's account page and show your app name and
the requested permissions. The user can either grant or deny the request. If granted, the NextPYP website will
generate an app token that you can use to authenticate the NextPYP client. This app token authorizes the client to
access the granted set of services and functions for that user only.

App tokens are a more secure alternative to having your app try to collect (and store!) the user's password to use
in automated login attempts. Not only is the app token scoped to specific services and functions (rather than
allowing user-equivalent access to any function), but it also identifes the app making the requests, allowing
users to integrate with multiple apps and allow them separate permissions. App tokens are also separate from the
user's actual NextPYP login credentials, meaning, for example, users do not have to reveal their password (or
third-party login credentials in the case of SSO) to app developers to allow integrations.


Usage
-----

Creating a Client
^^^^^^^^^^^^^^^^^

First, decide where your app will be deployed and how it can reach the NextPYP website from that location.
Let's say your deployed app can reach the NextPYP website at the URL: ``https://nextpyp.my.org``.

Next, create a client in unauthenticated mode to request the app token from a user, ``jeff`` by calling
the :py:meth:`.AppsService.request_token` function:

.. code-block:: python3

	from nextpyp.client import Client

	client = Client('https://nextpyp.my.org')


Version Compatibility
^^^^^^^^^^^^^^^^^^^^^

Now that you have a client, before you get started calling APIs, it's generally a good idea to check that your
client version is compatible with the server version. The NextPYP API is versioned with a dedicated version number
just for the API that is separate from the overall NextPYP version. This API version number follows
(as best as we can manage) the formal rules of `Semantic Versioning`_, which means this version number is specific
enough that we can use it to check for compatibility between client and server.

.. _Semantic Versioning: https://semver.org

The compatibility check is implemented in :py:meth:`.Client.is_compatible()`. Call that method to check
that your client version is compatible with the server version.

.. code-block:: python3

	if not client.is_compatible():
		raise Exception("Client might not work anymore, time to update")


Requesting Permissions
^^^^^^^^^^^^^^^^^^^^^^

Next, decide what services and functions your app will need to use and collect the permission ids.
Permission information can be found in the API documentation for each service and function.
Let's say your app needs to access the Frobnicator section of the NextPYP website and neeeds the following
permissions: ``['session_list', 'session_create']``.

.. code-block:: python3

	token_data = client.services.apps.request_token(
		user_id='jeff',
		app_name='My App',
		app_permission_ids=['session_list', 'session_create']
	)
	print(f'token data: {token_data}')

The above example will print output similar to the following.

.. code-block:: text

	AppTokenRequestData[request_id='the-request-id', app_name='My App', permissions=[AppPermissionData[...]]]

Once the token has been requested, the user (``jeff`` in this example) should approve the request
on the website and copy the app token into your app. The app token is just a string, so it should
be easy to transfer.


Using Regular Services
^^^^^^^^^^^^^^^^^^^^^^

Once you have the app token, you can use the client in authenticated mode to access the permissioned services
and functions.

.. code-block:: python3

	client = Client(
		url_base='https://nextpyp.my.org',
		credentials=Credentials(
			userid='jeff',
			token='the-app-token'
		)
	)

	sessions = client.services.single_particle_sessions.list('jeff')
	for session in sessions:
		print(f'Session ID: {session.session_id}')
		if session.args.finished is not None:
			print(f'\tFinished Name: {session.args.finished.name}')
		if session.args.next is not None:
			print(f'\tNext Name: {session.args.next.name}')

In the above example, we listed the current sessions. Notice how the session has two different names.
In NextPYP, all sessions (and project jobs too) have two sets of arguments:

* ``finished`` arguments are the arguments that were used the last time the session (or job) was run.
* ``next`` arguments are the arguments that will be used the next time the session (or job) will be run.

Once a session/job is run, the arguments in the ``next`` position are moved into the ``finished`` position
and the ``next`` position is cleared. Therefore, sessions/jobs that have never been run will typically
only have ``next`` arguments and not ``finished`` arguments. Conversely, sessions/jobs that have just been run
will have only ``finished`` arguments and no ``next`` arguments.
Distinguishing between finished and next arguments lets users edit the arguments for a session/job without
changing any existing results, and easily allows reverting any changes back to their previous values.

Next, we'll create a new single particle session:

.. code-block:: python3

	from nextpyp.client.args import block_args, PypArgValues, PypBlock
	from nextpyp.client.gen import SingleParticleSessionArgs

	pyp_args = PypArgValues.from_toml(block_args(PypBlock.SESSION_SINGLE_PARTICLE))
	pyp_args.data_path = '/foo/bar'
	pyp_args.scope_pixel = 1
	pyp_args.slurm_verbose = True
	pyp_args.slurm_memory = 2
	args = SingleParticleSessionArgs(
		'My new session',
		'groupid',
		pyp_args.write()
	)
	session = client.services.single_particle_sessions.create(args)

In the example above, all of the properties to ``pyp_args`` are arguments to the ``pyp`` program used
internally by NextPYP. To run session and jobs, you'll need some familiarity with the arguments for ``pyp``.
Then, just give your new session a name and pick a group ID.

.. tip::

	If you don't know the group ID you want to use already,
	you can list all of the current group IDs with :py:meth:`.SessionService.groups`.

Finally, you can start the main session daemon with :py:meth:`.SessionService.start`:

.. code-block:: python3

	from nextpyp.client.gen SessionDaemon

	client.services.sessions.start(session.session_id, SessionDaemon.Streampyp)

Once the session is running, you can listen to what it's doing in real time with
the real-time services.


Using Real-Time Services
------------------------

Real-time services in the NextPYP client use Python's `asyncio`_ capabilities to ensure messages can be
processed in the client just as soon as they've been sent by the server.

.. _asyncio: https://docs.python.org/3/library/asyncio.html

You can listen to messages from the newly-started session using the
:py:attr:`.RealtimeServices.single_particle_session` real-time service.
However, since sessions/jobs can start sending messages very quickly after starting, it's a good idea to start
listening to the session before starting it.

After creating the session, but before starting it, start listening to it by sending the
:py:class:`.RealTimeC2SListenToSession` message to the real-time service.
Then wait for incoming messages from the server:

.. code-block:: python3

	import asyncio
	from nextpyp.client.gen import (
		RealTimeC2SListenToSession,
		RealTimeS2CSessionStatus
	)

	async def listen_to_session(client, session_id):
		async with client.realtime_services.single_particle_session as srv:

			# send the listen message
			await srv.send_listen_to_session(RealTimeC2SListenToSession(session_id))

			# wait for incoming messages
			while True:
				try:
					msg = await srv.recv()
				except asyncio.CancelledError:
					break
				if type(msg) is RealTimeS2CSessionStatus:
					print(f'received status message: {msg}')
				else:
					print(f'received other message: {msg}')

The example above makes an ``async`` function that listens to the session. If you want to call the from an
``async`` context, start the task and then cancel it when you're finished listening. Since our ``async`` listener
is designed to run forever, we'll need to cancel it explicitly.

.. code-block:: python3

	future = listen_to_session(client, session_id)
	# do some stuff, like start the session, wait a bit, etc
	future.cancel()

Or, if you're currently in a sync context, you can start a new event loop to run the ``async`` listener,
but you'll have to poll the event loop manually to process the tasks:

.. code-block:: python3

	import asyncio

	loop = asyncio.new_event_loop()

	coro = listen_to_session(client, session_id)
	task = loop.create_task(coro)

	# do some stuff, like start the session, wait a bit, etc
	# but also poll the event loop inbetween the other things
	for _ in range(6):
		loop.run_until_complete(asyncio.sleep(1))

	task.cancel()
	loop.stop()
	loop.run_until_complete(task)
	loop.close()

.. note::

	``asyncio.Runner`` is available in Python 3.11 and newer and may simplify running async
	tasks from sync contexts.
