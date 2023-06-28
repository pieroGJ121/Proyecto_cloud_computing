<template>
  <header class="mb-0">
    <NavbarComponent />
    <slot name="NavExtra"></slot>
  </header>
  <BackgroundComponent />
  <slot name="MainContent"></slot>
  <FooterComponent />
</template>

<script>
import FooterComponent from "./FooterComponent.vue";
import BackgroundComponent from "./BackgroundComponent.vue";
import NavbarComponent from "./NavbarComponent.vue";

export default {
  name: "LayoutComponent",
  components: {
    FooterComponent,
    BackgroundComponent,
    NavbarComponent,
  },
  metaInfo: {
    script: [
      {
        src: "https://mdbootstrap.com/api/snippets/static/download/MDB5-Pro-Advanced_6.2.0/js/mdb.min.js",
        async: true,
        defer: true,
      },
      {
        src: "https://mdbootstrap.com/api/snippets/static/download/MDB5-Pro-Advanced_6.2.0/plugins/js/all.min.js",
        async: true,
        defer: true,
      },
      {
        src: "https://kit.fontawesome.com/2116c4358d.js",
        async: true,
        defer: true,
      },
    ],
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css?family=Lato:300,400,700&display=swap");
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css");
@import url("https://mdbootstrap.com/api/snippets/static/download/MDB5-Pro-Advanced_6.2.0/css/mdb.min.css");
@import url("https://mdbootstrap.com/api/snippets/static/download/MDB5-Pro-Advanced_6.2.0/plugins/css/all.min.css");
@import url("../css/main_parts/navbar.css");
@import url("../css/main_parts/nav_extra.css");
body {
  font-family: "Lato", sans-serif;
}
</style>
