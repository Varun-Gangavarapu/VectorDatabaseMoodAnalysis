// TODO: Function Calls
gsapTimeline();
locoMotiveScroll();
swiperJS();
image2Video();
svgAnimation();


pageTextPopupEffect("#page2");


// TODO: Event Functions

function locoMotiveScroll() {
  gsap.registerPlugin(ScrollTrigger);

  // Using Locomotive Scroll from Locomotive https://github.com/locomotivemtl/locomotive-scroll

  const locoScroll = new LocomotiveScroll({
    el: document.querySelector("#main"),
    smooth: true,
  });
  // each time Locomotive Scroll updates, tell ScrollTrigger to update too (sync positioning)
  locoScroll.on("scroll", ScrollTrigger.update);

  // tell ScrollTrigger to use these proxy methods for the "#main" element since Locomotive Scroll is hijacking things
  ScrollTrigger.scrollerProxy("#main", {
    scrollTop(value) {
      return arguments.length
        ? locoScroll.scrollTo(value, 0, 0)
        : locoScroll.scroll.instance.scroll.y;
    }, // we don't have to define a scrollLeft because we're only scrolling vertically.
    getBoundingClientRect() {
      return {
        top: 0,
        left: 0,
        width: window.innerWidth,
        height: window.innerHeight,
      };
    },
    // LocomotiveScroll handles things completely differently on mobile devices - it doesn't even transform the container at all! So to get the correct behavior and avoid jitters, we should pin things with position: fixed on mobile. We sense it by checking to see if there's a transform applied to the container (the LocomotiveScroll-controlled element).
    pinType: document.querySelector("#main").style.transform
      ? "transform"
      : "fixed",
  });

  // each time the window updates, we should refresh ScrollTrigger and then update LocomotiveScroll.
  ScrollTrigger.addEventListener("refresh", () => locoScroll.update());

  // after everything is set up, refresh() ScrollTrigger and update LocomotiveScroll because padding may have been added for pinning, etc.
  ScrollTrigger.refresh();
}

function login() {
  window.location.href = 'http://127.0.0.1:5000/login';
}


function pageTextPopupEffect(pageId) {
  gsap.from(`${pageId} .elem h1`, {
    y: 120,
    stagger: 0.5,
    duration: 1,
    scrollTrigger: {
      trigger: pageId,
      scroller: "#main",
      start: "top 40%",
      end: "top 37%",
      scrub: 2,
    },
  });
  gsap.from(`${pageId} .elem h2, ${pageId} .elem h4, ${pageId} .elem h3`, {
    y: 20,
    stagger: 0.2,
    duration: 0.5,
    scrollTrigger: {
      trigger: pageId,
      scroller: "#main",
      start: "top 80%",
      end: "top 60%",
      scrub: 2,
    },
  });
}

function image2Video() {
  const allImageBox = document.querySelectorAll("#page3-elements .box");
  allImageBox.forEach((box) => {
    const videoElem = box.querySelector("video");
    box.addEventListener("mouseenter", () => {
      videoElem.currentTime = 0;
      videoElem.play();
    });
    box.addEventListener("mouseleave", () => {
      videoElem.pause();
    });
  });
}

function swiperJS() {
  var swiper = new Swiper(".mySwiper", {
    slidesPerView: 4,
    spaceBetween: 15,
    speed: 10000,
    loop: true,
    autoplay: {
      delay: 1,
      duration: 1,
      disableOnInteraction: false,
    },
  });
}

function svgAnimation() {
  const trigger = document.getElementById("page5-video");

  const mainSvg = document.getElementById("mainSvg");
  const circleSvg = document.getElementById("circleSvg");

  gsap.to(circleSvg, {
    rotation: 250,
    transformOrigin: "50% 50%",
    duration: 2,
    ease: "circ.out",
    scrollTrigger: {
      trigger,
      scroller: "#main",
      start: "top 10%",
      end: "top 100%",
      scrub: 10,
    },
  });
}

function gsapTimeline() {
  const tl = gsap.timeline();

  tl.from("#loader h3", {
    opacity: 0,
    stagger: 0.5,
  })
    .from("#loader h3 span", {
      x: 40,
      opacity: 0,
      duration: 1.5,
      stagger: 0.1,
      ease: "power1.out",
    })
    .to("#loader h3", {
      x: -20,
      opacity: 0,
      delay: 0.5,
      duration: 0.5,
    })
    .to("#loader", {
      opacity: 0,
      duration: 1.5,
    })
    .from("#page1-content h1 span", {
      opacity: 0,
      y: 100,
      stagger: 0.1,
      delay: -0.5,
      duration: 0.5,
      ease: "power3.out",
    })
    .to("#loader", {
      display: "none",
      delay: -0.5,
    });
}
