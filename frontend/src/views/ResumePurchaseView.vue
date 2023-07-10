<template>
  <LayoutComponent>
    <template #Content>
      <div class="wrapper_resume">
        <div class="container_resume">
          <h1>¡Gracias por tu compra!</h1>

          <div class="thank-you">
            <p>
              Hemos enviado una copia de la orden de compra a tu correo
              electrónico &#x1F60A;
            </p>
          </div>

          <div class="order-details">
            <div class="image" id="game_image">
              <img :src="purchase_image" :alt="purchase_game" />
            </div>
            <div class="info">
              <div class="title" id="game_title">{{ purchase_game }}</div>
              <div class="purchase-date" id="purchase_date">
                Fecha de compra: {{ purchase_date }}
              </div>
              <div class="order-id" id="order_id">
                ID de compra: {{ purchase_id }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </LayoutComponent>
</template>

<script>
import LayoutComponent from "@/components/Layout.vue";
import { getPurchaseData } from "@/services/search.api";
import { verifier_login } from "@/services/login.api";

export default {
  name: "ResumePurchaseView",
  components: {
    LayoutComponent,
  },
  async mounted() {
    await verifier_login();
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get("id");
    console.log(id);
    const purchase = await getPurchaseData(id);
    console.log(purchase);
    //this.purchase_game = game.name;
    //this.purchase_image = game.cover;
  },
  data() {
    return {
      purchase_game: "Getting data...",
      purchase_date: "Getting data...",
      purchase_id: "Getting data...",
      purchase_image: "Getting data...",
    };
  },
};
</script>

<style scoped>
@import url("../css/resume/resume.css");
</style>
