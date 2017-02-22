$(document).ready(function() {

    // Use a "/test" namespace.
    // An application can open a connection on multiple namespaces, and
    // Socket.IO will multiplex all those connections on a single
    // physical channel. If you don't care about multiple channels, you
    // can set the namespace to an empty string.
    namespace = '/test';
    var d = new Date();

    var datestring = d.getHours() + ":" + d.getMinutes();
    // Connect to the Socket.IO server.
    // The connection URL has the following format:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

    // Event handler for new connections.
    // The callback function is invoked when a connection with the
    // server is established.
    socket.on('connect', function() {
        socket.emit('msg event', {data: datestring + ' : I\'m connected!'});
    });

    // Event handler for server sent data.
    // The callback function is invoked whenever the server emits data
    // to the client. The data is then displayed in the "Received"
    // section of the page.
    socket.on('my response', function(msg) {
        $('#log').append('<br>' + $('<div/>').text('' + msg.count + ': ' + msg.data).html());
    });

    // Interval function that tests message latency by sending a "ping"
    // message. The server then responds with a "pong" message and the
    // round trip time is measured.
    var ping_pong_times = [];
    var start_time;
    window.setInterval(function() {
        start_time = (new Date).getTime();
        socket.emit('my ping');
    }, 1000);

    // Handler for the "pong" message. When the pong is received, the
    // time from the ping is stored, and the average of the last 30
    // samples is average and displayed.
    socket.on('my pong', function() {
        var latency = (new Date).getTime() - start_time;
        ping_pong_times.push(latency);
        ping_pong_times = ping_pong_times.slice(-30); // keep last 30 samples
        var sum = 0;
        for (var i = 0; i < ping_pong_times.length; i++)
            sum += ping_pong_times[i];
        $('#ping-pong').text(Math.round(10 * sum / ping_pong_times.length) / 10);
    });

    // Handlers for the different forms in the page.
    // These accept data from the user and send it to the server in a
    // variety of ways
    
    function len_150(input) {
        if(input.length > 150) {
            alert('Please, enter less than 150 characters.');
            
        }
    }

    $('form#broadcast').submit(function(event) {
        len_150($('#broadcast_data').val());

        socket.emit('broadcast event', {data: datestring + ' : ' + $('#broadcast_data').val()});
        return false;
    });

    $('form#join').submit(function(event) {
        var room_name;
        
        if($('#join_room').val().length > 50) {
            alert('Please enter length less than 50 characters. Longer names would be trimmed to 50.')
            room_name = $('#join_room').val().substring(0, 50);
        } else {
            room_name = $('#join_room').val();
        }
        
        socket.emit('join', {room: room_name});
        return false; 
    });

    $('form#leave').submit(function(event) {
        var room_name;
        
        if($('#leave_room').val().length > 50) {
            alert('Please enter length less than 50 characters. Longer names would be trimmed to 50.')
            room_name = $('#leave_room').val().substring(0, 50);
        } else {
            room_name = $('#leave_room').val();
        }
        
 
        socket.emit('leave', {room: room_name});
        return false;
    });
    $('form#send_room').submit(function(event) {

        var room_name;
        
        if($('#send_room').val().length > 50) {
            alert('Please enter length less than 50 characters. Longer names would be trimmed to 50.')
            room_name = $('#send_room').val().substring(0, 50);
        } else {
            room_name = $('#send_room').val();
        }
        
        socket.emit('room event', {room: $('#room_name').val(), data: datestring + ' : ' + $('#room_data').val()});
        return false;
    });
    
    
    $('form#disconnect').submit(function(event) {
        socket.emit('disconnect request');
        return false;
    });

});

