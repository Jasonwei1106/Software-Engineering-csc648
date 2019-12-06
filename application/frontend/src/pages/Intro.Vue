<template>
  <div>
    <div>
      <q-card style="min-width: 370px;">
        <div class="q-pa-xs">
          <q-btn
            round
            color="secondary" icon="arrow_back"
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
              :src="groups[routeName].avatar"
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

    <div style="margin: 7em;">
      {{ groups[routeName].intro }}
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      routeName: this.$route.params.name,
      groups: {
        phyo: {
          avatar: '../statics/square_phyo.jpg',
          intro: `Hi, I'm Phyo Htut. I'm currently a graduate student for Energy Systems [MS] and in process of transferring to Computer Science [MS] at San Francisco State University (SFSU). I am the project lead for this class project.`
        },
        antonio: {
          avatar: '../statics/antonio.jpg',
          intro: `Hi, I'm Antonio Carmona. I'm currently an undergraduate Computer Science student at San Francisco State University. I manage the project's GitHub repository and MySQL database. Outside of programming, my hobbies include gaming and working with electronics.`
        },
        myles: {
          avatar: '../statics/myles.jpg',
          intro: `Hello, my name is Myles. Currently I am a graduate student in Embedded Electrical and Computer Systems. I enjoy cooking and bouldering.`
        },
        eduardo: {
          avatar: '../statics/IMG_8454.jpg',
          intro: `I am a computer science major and a senior at SFSU like everyone else in this class. I enjoy photography and film.`
        },
        jason: {
          avatar: '../statics/json.jpeg',
          intro: `I'm Jason Wei, last year in SFSU, major in Computer Science. Nothing too interesting about me, loves sports and games.`
        }
      }
    }
  },
  methods: {
    goBack: function () {
      this.$router.go(-1)
    },
    getRoute: function () {
      this.routeName = this.$route.params.name
    }
  },
  watch: {
    $route: 'getRoute'
  }
}
</script>

<style>

</style>
