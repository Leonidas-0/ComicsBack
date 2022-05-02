document.addEventListener('DOMContentLoaded', function () {
    try {
    var renders = document.querySelectorAll('.stars');
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
}
catch (error) {
  try {
    var renders = document.querySelector('.stars');
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  }
  catch (error) {
  }
}
try {
    Array.from(renders).forEach(function (render) {
      var rating = parseInt(render.dataset.rating)
      function renderstars(rating) {
        for (let j = 0; j < 5; j++) {
          {
            if (rating - 1 < j) {
              render.insertAdjacentHTML('beforeend', `<button class="rating">☆</button>`);
            } else {
              render.insertAdjacentHTML('beforeend', `<button class="rating">★</button>`);
            }
            render.querySelectorAll("button")[j].id = j;
            render.querySelectorAll("button")[j].addEventListener('click', () => {
              fetch(`/rate/${render.dataset.name}/${(j).toString()}`,
                {
                  method: 'POST',
                  headers: { 'X-CSRFToken': csrftoken },
                  mode: 'same-origin'
                }).then((response) => response.json()).then((result) => {
                  console.log(result)
                  if (result == "Rated previously!") {
                    render.previousElementSibling.innerHTML = "Rated previously!";
                    render.previousElementSibling.style.visibility = "visible";
                  }
                  else {
                    render.previousElementSibling.innerHTML = "Rated!";
                    render.previousElementSibling.style.visibility = "visible";
                    render.innerHTML = "",
                      renderstars(j + 1)
                  }
                })
            })
          }
        }
      } renderstars(rating)
    }
    )
 }
catch (error) 
{} })
