/* jshint esversion: 6, jquery: true */
$(document).ready(function() {
    const roomName = JSON.parse(document.getElementById('room_name').textContent);
    const socketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';

    const socket = new WebSocket(socketProtocol + '//' + window.location.host + '/ws/chat/' + roomName + '/');
    const messageContainer = $('.chat-messages');
    messageContainer.scrollTop(messageContainer.prop('scrollHeight'));

    const username = document.getElementById("username").value;
    const chatId = document.getElementById("chatId").value;

    
    const updateMessageStatusUrl = window.location.protocol + '//' + window.location.host + '/my_messages/update-message-read-status/';
    const updateMessageStatus = function(messageId) {
        $.ajax({
            url: updateMessageStatusUrl,
            type: 'POST',
            data: {
                'message_id': messageId,
                'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value
            },
            success: function(data) {
                console.log('Message status updated');
            },
            error: function(data) {
                console.log(data);
            }
        });
    };



    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const type = data.type;
        if (type === 'chat_message'){
            $('.no-messages').remove();

            const chatMessage = $('<div class="chat-message"></div>');
            const messageAuthor = $('<div class="message-author"></div>');
            if(data.sendBy===username){
                chatMessage.addClass('my-message');
            } else {
                chatMessage.addClass('other-message');
                updateMessageStatus(data.messageId);
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
            $(messageContainer).find('.typing').before(chatMessage);
            // check if .typing contains the message author and clear it
            if($('.typing').text().includes(data.author.username)){
                $('.typing').text('');
            }
        } else if (type === 'typing') {
            let userTyping = data.username;
            let profileName = data.profile_name;
            if (userTyping !== username) {
                let typingElement = $('.typing');
                if (typingElement.text() === '') {
                    typingElement.text(profileName + ' is typing...');
                    setTimeout(() => {
                        typingElement.text('');
                    } , 10000);
                }

            }
        } 
        // Scroll to the bottom of the chat messages
        messageContainer.scrollTop(messageContainer[0].scrollHeight + 1000);
        
    };

    socket.onclose = function(event) {
        console.log('Something went wrong');       
    };

    const sendMessage = () => {
        const message = $('.chat-input').val();
        
        // pick up line breaks and links
        let messageContent = message;
        messageContent = messageContent.replace(/\n/g, '<br>');
        // use linkifyjs to convert links to html
        messageContent = linkifyHtml(messageContent);
        if (message.length > 0) {
            socket.send(
              JSON.stringify({
                type: 'chat_message',
                message: messageContent,
                username: username,
                chatId: chatId
              })
            );
            $('.emojionearea-editor').html('');
            $('.chat-input').val('');
        }
    };

    const sendTyping = () => {
        socket.send(
            JSON.stringify({
                type: 'typing',
                username: username,
                chatId: chatId
            })
        );
    };

    $('.chat-send-button').click(sendMessage);
    // put a focus on the emojionearea-editor
    // $(".chat-input").data("emojioneArea").editor.focus();
    // send a message when the enter+ctrl key is pressed
    $(document).keydown(function(event) {
        if (event.keyCode === 13 && event.ctrlKey) {
            let message = $('.emojionearea-editor').html();
            // if there are div elements in the message, replace them with br tags
            message = message.replace(/<div>/g, '<br>');
            // and remove the closing div tag
            message = message.replace(/<\/div>/g, '');
            $('.chat-input').val(message);
            sendMessage();
        } 
    });
    $(document).keyup(function(event) {
        // if (!(event.keyCode === 13 && event.ctrlKey)) {
        //     sendTyping();
        // } 
        // check if user is typing inside the .chat-input or .emojionearea-editor
        if ($('.chat-input').is(':focus') || $('.emojionearea-editor').is(':focus')) {
            sendTyping();
        }
    } );

}); // end of document ready