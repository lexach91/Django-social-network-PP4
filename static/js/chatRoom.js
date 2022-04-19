$(document).ready(function() {
    const socketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';

    // socket will connect to the address that looks like:
    // ws://127.0.0.1:8080/my_messages/chat-with-<str:username>/
    const socket = new WebSocket(socketProtocol + '//' + window.location.host + window.location.pathname);

    const messageContainer = $('.chat-messages');
    messageContainer.scrollTop(messageContainer.prop('scrollHeight'));

    const username = document.getElementById("username").value;
    const chatId = document.getElementById("chatId").value;



    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log(data);
        const chatMessage = $('<div class="chat-message"></div>');
        const messageAuthor = $('<div class="message-author"></div>');
        if(data.sendBy===username){
            chatMessage.addClass('my-message');
        } else {
            chatMessage.addClass('other-message');
        }
        const messageText = $('<div class="message-text"></div>');
        const messageTime = $('<div class="message-time"></div>');
        let authorAvatar;
        if (data.author.avatar) {
            authorAvatar = $(
              '<img class="message-avatar" src="' + data.author.avatar + '" />'
            );
        } else {
            authorAvatar = $(
              '<img class="message-avatar" src="/static/images/default_avatar.svg" />'
            );
        }
        messageAuthor.append(authorAvatar);
        messageAuthor.append(data.author.username);
        messageText.append(data.message.content);
        messageTime.append(data.message.timestamp);
        chatMessage.append(messageAuthor);
        chatMessage.append(messageText);
        chatMessage.append(messageTime);
        messageContainer.append(chatMessage);

        // Scroll to the bottom of the chat messages
        messageContainer.scrollTop(messageContainer[0].scrollHeight + 1000);
        
    };

    socket.onclose = function(event) {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', event.reason);
        // setTimeout(function() {
        //     socket.connect();
        // }, 1000);
    }

    

    $('.chat-send-button').click(function() {
        const message = $('.chat-input').val();
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