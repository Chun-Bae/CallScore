function updateDropdownText() {
  const navbarDropdown = document.getElementById('navbarDropdown');
  const dropdownItems = document.querySelectorAll('.dropdown-menu a');
  console.log(navbarDropdown);
  console.log(dropdownItems); 

  const scrollPosition = window.scrollY;
  console.log(scrollPosition);
  let activeSection = null;
  
  for (const item of dropdownItems) {
    
    const section = document.querySelector(item.getAttribute('href'));
    const sectionTop = section.offsetTop;
    const sectionBottom = sectionTop + section.offsetHeight;
    const sectionMid = (sectionTop + sectionBottom) /2;
    

    
    if (scrollPosition >= sectionTop - sectionMid && scrollPosition < sectionMid) {
      activeSection = item.textContent;
      break;
    }
  }

  if (activeSection) {
    navbarDropdown.textContent = activeSection;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  updateDropdownText();
  window.addEventListener('scroll', updateDropdownText);
});


