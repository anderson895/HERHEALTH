

// Handle Enter key press
$('#user-input').on('keypress', function(event) {
    if (event.which === 13) {
        $('#send-btn').click();
    }
});

// Handle suggestions button click
$('.suggestion-btn').on('click', function() {
    const suggestion = $(this).data('suggestion');
    $('#user-input').val(suggestion);
    $('#send-btn').click();
});











function appendMessage(message, type) {
    const messageDiv = $('<div>').addClass('chat-message').addClass(type).addClass('mb-4 p-3 rounded-lg');
    if (type === 'user') {
        messageDiv.addClass('bg-[#444654] text-white text-right');
        messageDiv.text(message); // Display the user's message directly
    } else {
        messageDiv.addClass('text-white text-left');

        // Typing effect for the bot's message
        let index = 0;
        messageDiv.text('');
        $('#chat-box').append(messageDiv);
        $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);

        function typeWriter() {
            if (index < message.length) {
                messageDiv.append(message.charAt(index));
                index++;
                setTimeout(typeWriter, 50); // Adjust typing speed here
            }
        }

        typeWriter(); // Start the typing effect
    }

    $('#chat-box').append(messageDiv);
    $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
}





$('#send-btn').on('click', function() {
    const userMessage = $('#user-input').val().trim();
    if (userMessage) {
        $('#chat-box').show(); // Show the chat box when the first message is sent
        appendMessage(userMessage, 'user');  // Display the user's message directly
        $('#user-input').val('');

        $.ajax({
            url: '/chat',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ message: userMessage }),
            success: function(data) {
                const botResponse = data.response;

                // Check if the bot response contains an image URL
                if (data.image_url) {
                    // Create an <img> element and append it to the chat box
                    const imageElement = $('<img>').attr('src', data.image_url).addClass('w-full mt-2');
                    $('#chat-box').append(imageElement);
                } else {
                    // Otherwise, append the response message with typing effect
                    appendMessage(botResponse, 'bot');
                }
            },
            error: function(error) {
                console.error('Error:', error);
                appendMessage("Sorry, something went wrong. Please try again.", 'bot');
            }
        });
    }
});

