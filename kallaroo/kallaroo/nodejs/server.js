var http = require('http');
var server = http.createServer().listen(3000, function(){
	console.log("connected to port 3000");
});
var io = require('socket.io').listen(server);
var cookie_reader = require('cookie');
var querystring = require('querystring');


var redis = require('socket.io/node_modules/redis');


// Configure socket.io to store cookie set by Django
// io.use(function(){
// 	io.set('authorization', function(data, accept){
// 		if(data.headers.cookie){
// 			data.cookie = cookie_reader.parse(data.headers.cookie);
// 			return accept(null, true);
// 		}
// 		return accept('error', false);
// 	});
// 	io.set('log level', 1);
// });



io.sockets.on('connection', function(socket){
	// console.log('a user connected');
	// console.log(socket.id);
	// console.log("=============");
	var sub = redis.createClient();
	/*
	=================
	Realtime for Chatrooms
	=================
	*/

	socket.on('room-number', function(data){
		// console.log(data.room_id);
		// console.log("=======");
		// console.log("chatroom"+data.room_id);
		var channel = "chatroom"+data.room_id;
		console.log(channel);
		// subscribe to the redis channel
		sub.subscribe(channel);
	});
	
	// Grab message from Redis and send to client
	sub.on('message', function(channel, message){
		socket.send(message);

	});

	// listen to socket event named 'send-message'
	socket.on('send-message', function(data){

		// take the msg and send it to django backend to be saved
		var user_id = data.user_id;
		var msg = data.msg;
		var chatroom_id = data.chatroom_id;

		var postData = querystring.stringify({
			user_id: user_id,
			msg: msg,
			chatroom_id: chatroom_id,
		});

		/***** POST request for CHAT MSG *****/

		var options = {
		  hostname: '127.0.0.1',
		  port: 8000,
		  // must remove the trailing slash from path url & url in urls.py
		  path: '/chats/send-message',
		  method: 'POST',
		  headers: {
		    'Content-Type': 'application/x-www-form-urlencoded',
		    'Content-Length': postData.length
		  }
		};

		var req = http.request(options, function(res) {
		  // console.log('STATUS: ' + res.statusCode);
		  // console.log('HEADERS: ' + JSON.stringify(res.headers));
		  res.setEncoding('utf8');
		  res.on('data', function (chunk) {
		  	// JsonResponse returned by the view
		    console.log(chunk);

		  });
		  res.on('end', function() {
		    console.log('No more data in response.')
		  })
		});

		req.on('error', function(e) {
		  console.log('problem with request: ' + e.message);
		});

		// write data to request body
		req.write(postData);
		req.end();

		// socket.broadcast.to(id).emit('response-message',postData);

	});

	/*
	=================
	Realtime for bids
	=================
	- create a new client
	- When user goes to the TaskDetailView page, send a socket.emit containing taskid#
	- socket.on then subscribes client1 to new channel
	- When a bid is submitted, trigger a socket.emit
	- socket.on will pass information to the backend and save
	- send that data back through the redis channel
	*/

	var client1 = redis.createClient();
	socket.on('auction-number', function(data){
		var channel1 = "auction"+data.task_id;
		console.log("auction id is: " + channel1);
		client1.subscribe(channel1);
	})

	client1.on('message', function(channel1, bid){
		socket.send(bid);
	});

	

	/*
	======================
	Realtime Notifications
	======================
	*/
	socket.on('assign-socket-id', function(data){

		// get the socket.id
		// run a $.post request
		// send the socket.id in that POST request
		// on the backend, assign it to request.user and create a request.session['socket_id']
		// if 'socket_id' in request.session
		// should only assign request.session['socket_id'] after login() occurs 
		// don't run the .POST everytime the User goes to the dashboard page

		//console.log(data.user_id);
		var socket_id = socket.id;
		var user_id = data.user_id;

		var postData = querystring.stringify({
			socket_id: socket_id,
			user_id: user_id,
		});

		var options = {
		  hostname: '127.0.0.1',
		  port: 8000,
		  // must remove the trailing slash from path url & url in urls.py
		  // path: '/accounts/' + user_id + '/dashboard/',
		  path: '/accounts/assign-socket-id',
		  method: 'POST',
		  headers: {
		    'Content-Type': 'application/x-www-form-urlencoded',
		    'Content-Length': postData.length
		  }
		};

		var req = http.request(options, function(res) {
		  // console.log('STATUS: ' + res.statusCode);
		  // console.log('HEADERS: ' + JSON.stringify(res.headers));
		  res.setEncoding('utf8');
		  res.on('data', function (chunk) {
		  	// JsonResponse returned by the view
		    console.log(chunk);

		  });
		  res.on('end', function() {
		    console.log('No more data in response.')
		  })
		});

		req.on('error', function(e) {
		  console.log('problem with request: ' + e.message);
		});

		// write data to request body
		req.write(postData);
		req.end();

	});

	
	/* POST request for LOGIN */
	socket.on('assign-socket-id-after-login', function(){
		var socket_id = socket.id;
		var postData = querystring.stringify({
			socket_id: socket_id,
		});

		var options = {
		  hostname: '127.0.0.1',
		  port: 8000,
		  // change the path to match login_user
		  path: '/accounts/assign-socket-id',
		  method: 'POST',
		  // need to send the CSRF_TOKEN through again
		  headers: {
		    'Content-Type': 'application/x-www-form-urlencoded',
		    'Content-Length': postData.length
		  }
		};

		var req = http.request(options, function(res) {
		  // console.log('STATUS: ' + res.statusCode);
		  // console.log('HEADERS: ' + JSON.stringify(res.headers));
		  res.setEncoding('utf8');
		  res.on('data', function (chunk) {
		  	// JsonResponse returned by the view
		    console.log(chunk);

		  });
		  res.on('end', function() {
		    console.log('No more data in response.')
		  })
		});

		req.on('error', function(e) {
		  console.log('problem with request: ' + e.message);
		});

		// write data to request body
		req.write(postData);
		req.end();

	});


	/*
	===========================
	Notifications for New Task
	===========================
	*/

	// var client1 = redis.createClient();
	// socket.on('auction-number', function(data){
	// 	var channel1 = "auction"+data.task_id;
	// 	console.log("auction id is: " + channel1);
	// 	client1.subscribe(channel1);
	// })

	// client1.on('message', function(channel1, bid){
	// 	socket.send(bid);
	// });

	
	var task1 = redis.createClient();
	socket.on('new_task_added', function(data){
		// var msg = "A new task has been added.";
		console.log("new task has been added");
		// var taskChannel = data.subcategory + "_channel";
		var taskChannel = "new_task_1"
		console.log("this is the channel: " + taskChannel);
		task1.subscribe(taskChannel);

	});

	task1.on('message', function(taskChannel, notification){
		socket.send(notification);
		console.log("sending message: " + notification);
	});

});

