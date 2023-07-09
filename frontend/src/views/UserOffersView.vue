<template>
  <LayoutComponent>
    <template #Content> a </template>
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
    await verifier_login();
  },
};
</script>

<style></style>
