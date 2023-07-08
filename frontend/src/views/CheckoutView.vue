<template>
  <LayoutComponent>
    <template #Content>
      <div class="contenedor">
        <h1>Ya casi completas tu compra. Espera un momento por favor...</h1>
        <div class="spinner-box">
          <div class="configure-border-1">
            <div class="configure-core"></div>
          </div>
          <div class="configure-border-2">
            <div class="configure-core"></div>
          </div>
        </div>
      </div>
    </template>
  </LayoutComponent>
</template>

<script>
import LayoutComponent from "@/components/Layout.vue";
import { verifier_login } from "@/services/login.api";

export default {
  name: "IndexView",
  components: {
    LayoutComponent,
  },
  async mounted() {
    verifier_login();
    setTimeout(() => {
      window.location.href = "/resume" + window.location.search;
    }, 5000);
  },
};
</script>

<style scoped>
@import url("../css/wait/wait.css");
</style>
