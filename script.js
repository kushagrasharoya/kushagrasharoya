/* ======================================================
   KUSHAGRA SHAROYA PORTFOLIO
   JavaScript
====================================================== */


/* =====================================
   Typing Animation
===================================== */

const roles = [
    "Software Engineer",
    "Problem Solver",
    "Aspiring AI Engineer",
    "Open Source Learner",
    "Competitive Programmer",
    "Lifelong Learner"
];

const typingElement = document.getElementById("typing");

let roleIndex = 0;
let charIndex = 0;
let deleting = false;

function typeEffect(){

    const currentRole = roles[roleIndex];

    if(!deleting){

        typingElement.textContent =
        currentRole.substring(0,charIndex++);

        if(charIndex > currentRole.length){

            deleting = true;

            setTimeout(typeEffect,1200);

            return;

        }

    }

    else{

        typingElement.textContent =
        currentRole.substring(0,charIndex--);

        if(charIndex < 0){

            deleting = false;

            roleIndex++;

            if(roleIndex >= roles.length){

                roleIndex = 0;

            }

        }

    }

    setTimeout(typeEffect,deleting?40:80);

}

typeEffect();



/* =====================================
   Smooth Reveal Animation
===================================== */

const sections = document.querySelectorAll("section");

const observer = new IntersectionObserver(entries=>{

entries.forEach(entry=>{

if(entry.isIntersecting){

entry.target.classList.add("show");

}

})

},
{
threshold:.15
});

sections.forEach(section=>{

section.classList.add("hidden");

observer.observe(section);

});



/* =====================================
   Active Navbar
===================================== */

const navLinks=document.querySelectorAll("nav a");

window.addEventListener("scroll",()=>{

let current="";

sections.forEach(section=>{

const top=section.offsetTop-200;

const height=section.clientHeight;

if(pageYOffset>=top){

current=section.getAttribute("id");

}

});

navLinks.forEach(link=>{

link.classList.remove("active");

if(link.getAttribute("href")==="#"+current){

link.classList.add("active");

}

});

});



/* =====================================
   Back To Top Button
===================================== */

const topBtn=document.createElement("button");

topBtn.innerHTML="⬆";

topBtn.className="top-btn";

document.body.appendChild(topBtn);

window.addEventListener("scroll",()=>{

if(window.scrollY>500){

topBtn.style.display="block";

}

else{

topBtn.style.display="none";

}

});

topBtn.onclick=()=>{

window.scrollTo({

top:0,

behavior:"smooth"

});

};



/* =====================================
   Mouse Glow
===================================== */

const glow=document.createElement("div");

glow.className="cursor-glow";

document.body.appendChild(glow);

window.addEventListener("mousemove",e=>{

glow.style.left=e.clientX+"px";

glow.style.top=e.clientY+"px";

});



/* =====================================
   Navbar Blur
===================================== */

const nav=document.querySelector("nav");

window.addEventListener("scroll",()=>{

if(window.scrollY>100){

nav.classList.add("nav-scroll");

}

else{

nav.classList.remove("nav-scroll");

}

});



/* =====================================
   Button Ripple Effect
===================================== */

document.querySelectorAll("button").forEach(btn=>{

btn.addEventListener("click",function(e){

const ripple=document.createElement("span");

ripple.className="ripple";

const rect=this.getBoundingClientRect();

ripple.style.left=e.clientX-rect.left+"px";

ripple.style.top=e.clientY-rect.top+"px";

this.appendChild(ripple);

setTimeout(()=>{

ripple.remove();

},600);

});

});



/* =====================================
   Console Message
===================================== */

console.log(

"%cWelcome to Kushagra Sharoya's Portfolio 🚀",

"color:#3B82F6;font-size:20px;font-weight:bold;"

);

console.log(

"%cThanks for checking the code! 😊",

"color:white;font-size:14px;"

);
