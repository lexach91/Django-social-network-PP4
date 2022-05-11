/* jshint esversion: 6, jquery: true */
$(document).ready(function() {
    const roomName = JSON.parse(document.getElementById('room_name').textContent);
    const socketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';

    const socket = new WebSocket(socketProtocol + '//' + window.location.host + '/ws/chat/' + roomName + '/');

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
        let authorAvatar = $('<img class="message-avatar" src="' + data.author.avatar + '" />');
        
        messageAuthor.append(authorAvatar);
        messageAuthor.append(data.author.username);
        
        messageText.append(data.message.content);
        
        let time = moment.utc(data.message.timestamp, 'MMMM D, YYYY, h:mm a').fromNow();
        
        // let time = moment(data.message.timestamp).fromNow();
        messageTime.append(time);
        
        // messageTime.append(data.message.timestamp);
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
    };

    const sendMessage = () => {
        const message = $('.chat-input').val();
        
        console.log(message);
        // pick up line breaks and links
        let messageContent = message;
        messageContent = messageContent.replace(/\n/g, '<br>');
        // use linkifyjs to convert links to html
        messageContent = linkifyHtml(messageContent);
        // console.log(username);
        if (message.length > 0) {
            socket.send(
              JSON.stringify({
                message: messageContent,
                username: username,
                chatId: chatId
              })
            );
            $('.emojionearea-editor').html('');
            $('.chat-input').val('');
        }
    };

    

    $('.chat-send-button').click(sendMessage);
    // put a focus on the emojionearea-editor
    // $(".chat-input").data("emojioneArea").editor.focus();
    // send a message when the enter+ctrl key is pressed
    $(document).keydown(function(event) {
        console.log(event.keyCode);
        if (event.keyCode === 13 && event.ctrlKey) {
            let message = $('.emojionearea-editor').html();
            // if there are div elements in the message, replace them with br tags
            message = message.replace(/<div>/g, '<br>');
            // and remove the closing div tag
            message = message.replace(/<\/div>/g, '');
            $('.chat-input').val(message);
            sendMessage();
            console.log('send message');
        }
    }
    );

}); // end of document ready