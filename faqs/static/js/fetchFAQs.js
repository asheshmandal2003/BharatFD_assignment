const faqList = document.getElementById("faq-list");
const langSelect = document.getElementById("lang");
const search_btn = document.querySelector(".search_btn");
const loadMoreBtn = document.getElementById("load-more-btn");
let currentPage = 1;

function fetchFAQs(page = 1) {
  const lang = langSelect.value;
  fetch(`/api/v1/faqs/?lang=${lang}&page=${page}`)
    .then((response) => response.json())
    .then((data) => {
      if (page === 1) {
        faqList.innerHTML = "";
      }

      if (data.results.length === 0) {
        faqList.innerHTML = "<p>No FAQs available.</p>";
        loadMoreBtn.style.display = "none";
        return;
      }

      data.results.forEach((faq) => {
        faqList.innerHTML += `
          <div class="faq-item">
            <strong class="faq-item-question">Q: ${faq.question}</strong><br>
            <strong class="faq-item-answer">Answer:</strong> ${faq.answer}
          </div>
        `;
      });

      if (data.next) {
        loadMoreBtn.style.display = "block";
      } else {
        loadMoreBtn.style.display = "none";
      }

      currentPage = page;
    })
    .catch(() => {
      faqList.innerHTML =
        "<p>An error occurred while fetching FAQs. Please try again later.</p>";
      loadMoreBtn.style.display = "none";
    });
}

loadMoreBtn.addEventListener("click", () => {
  currentPage += 1;
  fetchFAQs(currentPage);
});

search_btn.addEventListener("click", () => {
  currentPage = 1;
  fetchFAQs(currentPage);
});

langSelect.addEventListener("change", () => {
  currentPage = 1;
  fetchFAQs(currentPage);
});

fetchFAQs(currentPage);
