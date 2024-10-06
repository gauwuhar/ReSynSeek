function showLoginForm() {
    const loginFormContainer = document.querySelector('.login-form-container');
    loginFormContainer.classList.add('active');
}

function closeLoginForm() {
    const loginFormContainer = document.querySelector('.login-form-container');
    loginFormContainer.classList.remove('active');
}


// --------------------------------------------------- скрыть показать секцию
$("button.show-section-btn").click(function() {
    $("#hideworks, #hidecart, #hidefooter").slideDown();
});

$("button.hide-section-btn").on("click", function() {
    $("#hideworks, #hidecart, #hidefooter").fadeOut();
});


$(document).ready(function() {
    // Show the corresponding video player when clicking the "Show Player" button
    $("button.show-section-btn").click(function() {
        const movieId = $(this).data("movie-id");
        $(`#hideworks_${movieId}`).slideDown();
    });

    // Hide the corresponding video player when clicking the "Hide Player" button
    $("button.hide-section-btn").on("click", function() {
        const movieId = $(this).data("movie-id");
        $(`#hideworks_${movieId}`).fadeOut();
    });
});