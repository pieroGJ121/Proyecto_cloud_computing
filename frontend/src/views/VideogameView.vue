<template>
  <LayoutComponent>
    <template #Content>
      <div id="container">
        <div id="game_details">
          <div id="left_column">
            <div id="game_image">
              <img :src="game_image" :alt="game_name" />
            </div>
            <div id="synopsis">
              <h2>Sinopsis</h2>
              <p id="synopsis_p">
                {{ game_synopsis }}
              </p>
            </div>
          </div>
          <div id="right_column">
            <div id="game_info">
              <h3 id="game_name">{{ game_name }}</h3>
              <div id="year">Fecha de publicación: {{ game_year }}</div>
              <div id="genre">
                Generos:
                {{ game_genre }}
              </div>
              <div id="publisher">Editores: {{ game_publisher }}</div>
              <div id="platform">
                Plataformas:
                {{ game_platform }}
              </div>
            </div>
            <div id="score_container">
              <h4>Puntaje</h4>
              <div id="avg">{{ avg }} ({{ amount }} puntajes)</div>
            </div>
            <div class="sell-card-button">
              <button @click="publishRating">Añade tu puntaje</button>
            </div>

            <div id="offers_container">
              <h4>Reseñas disponibles</h4>
              <div class="sell-card-button">
                <button @click="publishReview">Añade tu reseña</button>
              </div>
              <div
                class="offer-card"
                v-for="review in reviews"
                :key="review.id"
              >
                <div class="seller">
                  {{ review.usuario_name }}
                </div>
                <div class="price">{{ review.title }}</div>
                <div class="date-publish">
                  {{ review.comment }}
                </div>
              </div>
              <div id="buy_message" v-if="this.reviews.length === 0">
                No hay reseñas disponibles para este título
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
import { getGameData } from "@/services/search.api";
import { verifier_login } from "@/services/login.api";
import { getRatingGame } from "@/services/rating.api";
import { getReviewsGame } from "@/services/review.api";

export default {
  name: "VideogameView",
  components: {
    LayoutComponent,
  },
  methods: {
    publishRating() {
      const urlParams = new URLSearchParams(window.location.search);
      const id = urlParams.get("id");
      window.location.href = "/new_rating?id=" + id;
    },
    publishReview() {
      const urlParams = new URLSearchParams(window.location.search);
      const id = urlParams.get("id");
      window.location.href = "/new_review?id=" + id;
    },
  },
  data() {
    return {
      game_id: "Getting data...",
      game_name: "Getting data...",
      game_year: "Getting data...",
      game_genre: "Getting data...",
      game_publisher: "Getting data...",
      game_platform: "Getting data...",
      game_synopsis: "Getting data...",
      game_image: "Getting data...",
      avg: 0,
      amount: 0,
      reviews: [],
    };
  },
  async mounted() {
    await verifier_login();
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get("id");
    const game = await getGameData(id);
    this.game_id = game.game.api_id;
    this.game_name = game.game.name;
    this.game_year = game.game.release_year;
    this.game_genre = game.game.genres;
    this.game_genre = this.game_genre.join(", ");
    this.game_publisher = game.game.involved_companies;
    this.game_publisher = this.game_publisher.join(", ");
    this.game_platform = game.game.platforms;
    this.game_platform = this.game_platform.join(", ");
    this.game_synopsis = game.game.summary;
    this.game_image = game.game.cover;
    const reviews_temp = await getReviewsGame(this.game_id);
    this.reviews = reviews_temp.reviews;
    const score = await getRatingGame(this.game_id);
    console.log(this.game_id);
    this.amount = score.amount == 0 ? 0 : score.amount;
    this.avg = score.avg;
  },
};
</script>

<style>
@import url("../css/game/game.css");
</style>
