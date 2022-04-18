$(document).ready(function() {
    const socketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';

    // socket will connect to the address that looks like:
    // ws://127.0.0.1:8080/my_messages/chat-with-<str:username>/
    const socket = new WebSocket(socketProtocol + '//' + window.location.host + window.location.pathname);

    const messageContainer = $('.chat-messages');

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log(data);
        if (data.type === 'chat_message') {
            const chatMessage = $('<div class="chat-message"></div>');
            const messageAuthor = $('<div class="message-author"></dive>');
            
        }
    }

    socket.onclose = function(event) {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', event.reason);
        // setTimeout(function() {
        //     socket.connect();
        // }, 1000);
    }

    

    $('.chat-send-button').click(function() {
        const message = $('.chat-input').val();
        const username = document.getElementById('username').value;
        const chatId = document.getElementById('chatId').value;
        // console.log(username);
        if (message.length > 0) {
            socket.send(
              JSON.stringify({
                message: message,
                username: username,
                chatId: chatId
              })
            );
            $('.chat-input').val('');
        }
    }
    );

})