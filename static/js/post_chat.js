$(document).ready(function () {
    $('#toggle-suggestions').click(function () {
        $('#suggestions-section').slideToggle('fast');

        // Rotate the arrow icon
        $('#toggle-icon').toggleClass('rotate-180');
    });


    $("#ShowSettingModal").click(function (e) { 
        e.preventDefault();
       
        $("#settings-modal").fadeIn();
    });
    
    $("#close-settings").click(function (e) { 
        $("#settings-modal").fadeOut();
    });

     // Close Modal when clicking outside the modal content
   $("#settings-modal").click(function(event) {
        if ($(event.target).is("#settings-modal")) {
            $("#settings-modal").fadeOut();
        }
    });

});




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
    if (type === 'user') {
        const userDiv = $('<div>')
            .addClass('chat-message user mb-4 p-3 rounded-lg bg-[#444654] text-white text-right')
            .text(message);
        $('#chat-box').append(userDiv);
        $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
    } else {
        const container = $('<div>')
            .addClass('chat-message bot mb-4 p-3 rounded-lg text-white text-left');

        const messageDiv = $('<div>');
        container.append(messageDiv);
        $('#chat-box').append(container);
        $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);

        let index = 0;

        function typeWriter() {
            if (index < message.length) {
                let char = message.charAt(index);

                // Handle new lines and bullets smoothly
                if (char === '\n') {
                    messageDiv.append('<br>');
                } else {
                    messageDiv.append(document.createTextNode(char));
                }

                index++;
                $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
                setTimeout(typeWriter, 30); // Adjust typing speed here
            }
        }

        typeWriter(); // Start the smooth typing effect
    }
}




$('#send-btn').on('click', function() {
    const userMessage = $('#user-input').val().trim();
    if (userMessage) {
        $('#chat-box').show(); 
        appendMessage(userMessage, 'user');  
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

