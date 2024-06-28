document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.star-rating label');
    stars.forEach(star => {
      star.addEventListener('click', function () {
        const allStars = star.parentElement.querySelectorAll('label');
        allStars.forEach(s => s.style.color = '#ddd');
        star.style.color = '#f5b301';
        let prev = star.previousElementSibling;
        while (prev) {
          prev.style.color = '#f5b301';
          prev = prev.previousElementSibling;
        }
      });
    });
  });