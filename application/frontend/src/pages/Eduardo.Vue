<template>
  <div>
    <div>
      <q-card>
        <div class="q-pa-xs">
          <q-btn
            color="secondary"
            round
            icon="arrow_back"
            @click="goBack"
          />
        </div>
        <q-card-section>
          <q-avatar
            size="200px"
            style="
              padding-top: 40px;
              margin-left: 42%;
            "
          >
            <q-img
              src="../statics/IMG_8454.jpg"
              class="avatar"
              style="
                max-width: 400px;
                height: 200px;
              "
            />
          </q-avatar>
        </q-card-section>
      </q-card>
    </div>

    <div
      style="
        padding: 40px;
        margin: 100px;
      "
    >
      {{ intro }}
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      intro: `I am a computer science major and a senior at SFSU like everyone else in this class. I enjoy photography and film.`
    }
  },
  methods: {
    goBack () {
      this.$router.go(-1)
    }
  }
}
</script>

<style>

</style>
