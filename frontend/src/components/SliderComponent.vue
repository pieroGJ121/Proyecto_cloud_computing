<template>
  <section class="wow fadeIn example no-padding no-transition slider-top">
    <div class="slider_wrapper">
      <div id="slider1_container">
        <div data-u="loading" class="jssorl-009-spin">
          <img
            class="load-ico"
            src="https://www.jssor.com/theme/svg/loading/static-svg/spin.svg"
          />
        </div>

        <div data-u="slides" class="slides-i">
          <div>
            <img data-u="image" src="../images/Slide_1.png" class="slider" />
          </div>
          <div>
            <img data-u="image" src="../images/Slide_2.png" class="slider" />
          </div>
          <div>
            <img data-u="image" src="../images/Slide_3.png" class="slider" />
          </div>
        </div>

        <div
          data-u="navigator"
          class="jssorb031"
          data-autocenter="1"
          data-scale="0.5"
          data-scale-bottom="0.75"
        >
          <div data-u="prototype" class="i">
            <svg viewBox="0 0 16000 16000" class="arrow-i1">
              <circle class="b" cx="8000" cy="8000" r="5800"></circle>
            </svg>
          </div>
        </div>

        <div
          data-u="arrowleft"
          class="jssora051"
          id="arrow1"
          data-autocenter="2"
          data-scale="0.75"
          data-scale-left="0.75"
        >
          <svg viewBox="0 0 16000 16000" class="arrow-i1">
            <polyline
              class="a"
              points="11040,1920 4960,8000 11040,14080 "
            ></polyline>
          </svg>
        </div>
        <div
          data-u="arrowright"
          class="jssora051"
          id="arrow2"
          data-autocenter="2"
          data-scale="0.75"
          data-scale-right="0.75"
        >
          <svg viewBox="0 0 16000 16000" class="arrow-i1">
            <polyline
              class="a"
              points="4960,1920 11040,8000 4960,14080 "
            ></polyline>
          </svg>
        </div>
      </div>
    </div>
  </section>
</template>
<script>
export default {
  name: "SliderComponent",
};
</script>
<style>
@import url("../css/index/slider_style.css");
@import url("../css/index/slider_extra.css");
</style>
