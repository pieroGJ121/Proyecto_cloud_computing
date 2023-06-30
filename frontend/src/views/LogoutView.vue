<template>
  <h1>Wait a second pls...</h1>
</template>
<script>
import { logout } from "@/services/login.api";
export default {
  name: "LogoutView",
  async mounted() {
    logout();
  },
};
</script>
