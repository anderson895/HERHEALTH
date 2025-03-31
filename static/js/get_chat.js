$(document).on("click", ".chat-date", function () {
    let selectedDate = $(this).data("date");
    let today = new Date().toISOString().split('T')[0];

    // Check if the clicked date is today and the current route is /user/explore
    if (window.location.pathname === "/user/explore") {
        window.location.href = "/user/home";
    }
});



function loadChatHistory() {
    // Show the spinner
    $("#spinner").show();

    $.ajax({
        url: "/api/chat_dates",
        type: "GET",
        dataType: "json",
        success: function (data) {
            $("#chat-history").empty();

            if (!data.chat_dates || data.chat_dates.length === 0) {
                $("#chat-history").append("<li class='py-1'>No chat history available.</li>");
            } else {
                let today = new Date().toISOString().split('T')[0]; // Get today's date in YYYY-MM-DD format
                data.chat_dates.forEach(date => {
                    // Check if the date is today's date and display "DATE TODAY"
                    let displayDate = (date === today) ? "DATE TODAY" : date;
                    $("#chat-history").append(`<li class="py-1 hover:text-white cursor-pointer chat-date" data-date="${date}">${displayDate}</li>`);
                });
            }

            $("#spinner").hide();
        },
        error: function () {
            $("#chat-history").append("<li class='py-1 text-red-500'>Error fetching chat history.</li>");
            $("#spinner").hide();
        }
    });
}

// Click event for fetching chats on specific date
$(document).on("click", ".chat-date", function () {
    let selectedDate = $(this).data("date"); // Get the selected date
    console.log("Selected Date: ", selectedDate);  // Debugging line to ensure the date is selected
    $("#target_date").val(selectedDate); // Set the hidden input to selected date
    fetchChats();  // Fetch chats based on the selected date
});

// Fetch chats using the current target date
function fetchChats() {
    let targetDate = $("#target_date").val(); // Get the target date from the hidden input
    console.log("Fetching Chats for Date: ", targetDate);  // Debugging line

    // Show the spinner before the request
    $("#spinner").show();

    $.ajax({
        url: "/get_chats",
        type: "GET",
        data: { target_date: targetDate },  // Send selected date
        dataType: "json",
        success: function (response) {
            $("#chat-box").empty();  // Clear chat content

            if (!response.chats || response.chats.length === 0) {
                $("#chat-box").append("<div class='py-1'>No chats available for this date.</div>");
            } else {
                // Loop through and display the chats
                response.chats.forEach(chat => {
                    let userMessage = `<div class="mb-4 p-3 rounded-lg bg-[#444654] text-white text-right">${chat.user_message}</div>`;
                    
                    let botMessage = "";
                    if (chat.bot_type === "text") {
                        botMessage = `<div class="mb-4 p-3 rounded-lg text-white text-left">${chat.bot_message}</div>`;
                    } else if (chat.bot_type === "img_url") {
                        botMessage = `<img src="${chat.bot_message}" class="w-full mt-2" alt="Bot Image" />`;
                    }

                    $("#chat-box").append(userMessage + botMessage);
                });
            }

            // Display the chat box after loading
            $("#chat-box").show();

            // Auto-scroll the chat box to the bottom if the user is at the bottom
            let chatBox = $("#chat-box");
            let isScrolledToBottom = chatBox.scrollTop() + chatBox.innerHeight() >= chatBox[0].scrollHeight - 10;
            if (isScrolledToBottom) {
                chatBox.scrollTop(chatBox[0].scrollHeight);
            }

            // Hide the spinner after data is loaded
            $("#spinner").hide();
        },
        error: function () {
            $("#chat-box").append("<div class='py-1 text-red-500'>Error fetching chats.</div>");
            $("#spinner").hide(); // Hide the spinner on error
        }
    });
}

loadChatHistory(); // Load chat dates on page load






$(document).ready(function () {

    var target_date = $("#target_date").val();


    console.log(target_date);

    function fetchChatHistory() {
        $.ajax({
            url: "/get_chats",
            type: "GET",
            data: { "target_date": target_date },
            dataType: "json",
            success: function (data) {
                if (!data.chats || data.chats.length === 0) {
                    $("#chat-box").hide();
                    return;
                }
    
                $("#chat-box").empty().show();
    
                data.chats.forEach(chat => {
                    let userMessage = `<div class="mb-4 p-3 rounded-lg bg-[#444654] text-white text-right">${chat.user_message}</div>`;
                    
                    let botMessage = "";
                    if (chat.bot_type === "text") {
                        botMessage = `<div class="mb-4 p-3 rounded-lg text-white text-left">${chat.bot_message}</div>`;
                    } else if (chat.bot_type === "img_url") {
                        botMessage = `<img src="${chat.bot_message}" class="w-full mt-2" alt="Bot Image" />`;
                    }
    
                    $("#chat-box").append(userMessage + botMessage);
                });
    
                // Only auto-scroll if the user is already at the bottom
                let chatBox = $("#chat-box");
                let isScrolledToBottom = chatBox.scrollTop() + chatBox.innerHeight() >= chatBox[0].scrollHeight - 10;
    
                if (isScrolledToBottom) {
                    chatBox.scrollTop(chatBox[0].scrollHeight);
                }
            },
            error: function (xhr, status, error) {
                console.error("❌ Failed to fetch chat history:", error);
                alert("Failed to load chat history. Please try again.");
            }
        });
    }
    



fetchChatHistory(); 


});