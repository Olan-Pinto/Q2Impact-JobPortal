console.log("Welcome Page Loaded");

// scripts.js
function toggleLanguage() {
  const langToggle = document.getElementById("languageToggle");
  const newLang = langToggle.checked ? "ar" : "en";

  // Store the selected language in localStorage
  localStorage.setItem("language", newLang);

  // Update the language for the whole page
  document.documentElement.setAttribute("lang", newLang);
  loadLanguage(newLang);
}

function loadLanguage(language) {
  fetch(`../languages/${language}.json`)
      .then((response) => response.json())
      .then((data) => {
          for (const key in data) {
              const element = document.getElementById(key);
              if (element) {
                  element.textContent = data[key];
              }
          }
      })
      .catch((error) => console.error("Error loading language file:", error));
}

document.addEventListener("DOMContentLoaded", () => {
  const languageToggle = document.getElementById("languageToggle");

  const urlParams = new URLSearchParams(window.location.search);
  const urlLanguage = urlParams.get("lang");
  const currentLanguage = urlLanguage || localStorage.getItem("language") || "en";

  localStorage.setItem("language", currentLanguage);
  languageToggle.checked = currentLanguage === "ar";

  loadLanguage(currentLanguage);

  languageToggle.addEventListener("change", () => {
      const newLanguage = languageToggle.checked ? "ar" : "en";
      localStorage.setItem("language", newLanguage);
      loadLanguage(newLanguage);
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const navigateBtn = document.getElementById("navigate-btn");
  if (navigateBtn) {
      navigateBtn.addEventListener("click", () => {
          const currentLanguage = localStorage.getItem("language") || "en";
          window.location.href = `employer.html?lang=${currentLanguage}`;
      });
  }
});

// Employment Data
fetch('http://127.0.0.1:5000/api/employment')
  .then(response => response.json())
  .then(data => {
    Plotly.newPlot('chart1', [{
      x: data.sectors,
      y: data.counts,
      type: 'bar',
      marker: { color: 'rgba(55, 128, 191, 0.7)' }
    }], {
      title: 'Employment by Sector',
      xaxis: { title: 'Sectors' },
      yaxis: { title: 'Number of Employees' }
    });
  })
  .catch(error => console.error('Error fetching employment data:', error));

// Distribution of Economic Sectors
fetch('http://127.0.0.1:5000/api/economic_sectors')
  .then(response => response.json())
  .then(data => {
    Plotly.newPlot('chart2', [{
      labels: data.sectors,
      values: data.percentages,
      type: 'pie'
    }], { 
      title: 'Distribution of Economic Sectors',
      margin: { t: 40, b: 40, l: 40, r: 40 }
    });
  })
  .catch(error => console.error('Error fetching economic sector data:', error));

// Position Types
fetch('http://127.0.0.1:5000/api/position_types')
  .then(response => response.json())
  .then(data => {
    Plotly.newPlot('chart3', [{
      x: data.types,
      y: data.counts,
      type: 'bar',
      marker: { color: ['#ff6b6b', '#4ecdc4'] }
    }], { 
      title: 'Position Types',
      margin: { t: 40, b: 40, l: 40, r: 40 }
    });
  })
  .catch(error => console.error('Error fetching position types data:', error));

// Vacancies by Governorate
fetch('http://127.0.0.1:5000/api/vacancies')
  .then(response => response.json())
  .then(data => {
    Plotly.newPlot('chart4', [{
      labels: data.governorates,
      values: data.counts,
      type: 'pie'
    }], { 
      title: 'Current Vacancies by Governorate',
      margin: { t: 40, b: 40, l: 40, r: 40 }
    });
  })
  .catch(error => console.error('Error fetching vacancies data:', error));

// Dynamic Example: Random Data Updates
setInterval(() => {
  const randomValue = Math.floor(Math.random() * 100);
  Plotly.update('chart3', {
    y: [[randomValue]],
  }, {}, 0);
}, 2000);

document.addEventListener('DOMContentLoaded', () => {
  const loginBtn = document.getElementById('login-btn');
  const signupBtn = document.getElementById('signup-btn');
  const loginForm = document.getElementById('login-form');
  const signupForm = document.getElementById('signup-form');

  // Toggle between Login and Signup forms
  loginBtn.addEventListener('click', () => {
      loginBtn.classList.add('active');
      signupBtn.classList.remove('active');
      loginForm.classList.remove('hidden');
      signupForm.classList.add('hidden');
  });

  signupBtn.addEventListener('click', () => {
      signupBtn.classList.add('active');
      loginBtn.classList.remove('active');
      signupForm.classList.remove('hidden');
      loginForm.classList.add('hidden');
  });
});
