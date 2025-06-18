function menubar() {
    var hihu = document.querySelector('.menu-data');
    var element = document.getElementById('Menu-bar');

    if (hihu) {
        hihu.classList.remove('animate__fadeOut');
        element.style.display = 'none';
        hihu.style.zIndex = '1';
        hihu.classList.add('animate__fadeIn');
    }
}

function closebar() {
    var hihu = document.querySelector('.menu-data');
    var element = document.getElementById('Menu-bar');
    if (hihu) {
        hihu.classList.remove('animate__fadeIn');
        hihu.style.zIndex = '-20';
        element.style.display = 'block';
        hihu.classList.add('animate__fadeOut');
    }
}

// Handle form submission via AJAX
document.getElementById('contact-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    fetch('/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email, message }),
    })
        .then(response => response.text())
        .then(data => {
            alert('Thank you for your message!');
            console.log('Server response:', data);
        })
        .catch((error) => {
            alert('Something went wrong.');
            console.error('Error submitting form:', error);
        });
});
