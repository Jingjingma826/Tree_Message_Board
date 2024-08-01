// message scripts
document.addEventListener('DOMContentLoaded', function() {
    var alertMessage = document.getElementById('alert-message');
    if (alertMessage) {
        var message = alertMessage.getAttribute('data-message');
        if (message) {
            alert(message);
        }
    }
});


function toggleReplies(messageId) {
    var repliesDiv = document.getElementById('replies-' + messageId);
    repliesDiv.style.display = (repliesDiv.style.display === 'none') ? 'block' : 'none';
}

function toggleReplyForm(id) {
    var replyFormDiv = document.getElementById('reply-form-' + id);
    replyFormDiv.style.display = (replyFormDiv.style.display === 'none') ? 'block' : 'none';
}



// profile scripts

document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("successModal");
    var span = document.getElementsByClassName("close")[0];
    var reloginButton = document.getElementById("reloginButton");

    if (modal) {
        modal.style.display = "block";

        span.onclick = function() {
            modal.style.display = "none";
        };

        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        };

        reloginButton.onclick = function() {
            window.location.href = logoutUrl;  // Use the global variable
        };
    }

    const dateInput = document.getElementById("birth_date");

    dateInput.addEventListener("input", function() {
        const datePattern = /^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])\/\d{4}$/;
        const dateValue = dateInput.value;

        if (!datePattern.test(dateValue)) {
            dateInput.setCustomValidity("Please enter the date in DD/MM/YYYY format.");
        } else {
            dateInput.setCustomValidity("");
        }
    });
});

// register scripts
function validatePasswords() {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirm_password").value;
    if (password !== confirmPassword) {
        alert("Passwords do not match. Please try again.");
        return false; // Prevent form submission
    }
    return true; // Allow form submission
}
