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
              src="../statics/antonio.jpg"
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

    <div style="padding: 40px; margin: 100px;">
      {{ intro }}
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      intro: `Hi, I'm Antonio Carmona. I'm currently an undergraduate Computer Science student at San Francisco State University. I manage the project's GitHub repository and MySQL database. Outside of programming, my hobbies include gaming and working with electronics.`
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
