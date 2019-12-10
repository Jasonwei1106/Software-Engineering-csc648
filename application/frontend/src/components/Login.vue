<template>
  <div
    class="q-pa-md bg-grey-3"
    style="width: 30vw; max-width: 500px; min-width: 270px;"
  >
    <div align="center">
      <strong>LOGIN</strong>
      <br><br>
    </div>

    <q-form @submit="onSubmit">
      <div>
        <div class="q-mb-sm">
          <q-input
            dense outlined
            bg-color="white"
            type="text"
            placeholder="USERNAME"
            v-model="logIn.username"
          />
        </div>

        <div class="q-mb-sm">
          <q-input
            dense outlined
            bg-color="white"
            type="password"
            placeholder="PASSWORD"
            v-model="logIn.password"
          />
        </div>
      </div>

      <div align="center">
        <div class="q-mb-md">
          <q-btn
            class="full-width"
            type="submit"
            color="primary"
            label="LOG IN"
          />
          <br>
        </div>

        <router-link to="/forgot">
          <span>FORGOT PASSWORD?</span>
        </router-link>
        <br>

        <router-link to="/register">
          <span @click="emitClose">SIGN UP HERE!</span>
        </router-link>
      </div>
    </q-form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  components: {
  },
  data () {
    return {
      logIn: {}
    }
  },
  methods: {
    onSubmit: function () {
      axios.post('http://54.67.109.241:5000/api/login', {
        username: this.logIn.username,
        password: this.logIn.password
      })
        .then(res => {
          this.$q.notify({
            icon: 'done',
            color: 'positive',
            message: 'Welcome back!'
          })

          this.$q.localStorage.set('__diyup__signedIn', res.data.token)
          this.$q.localStorage.set('__diyup__username', this.logIn.username)

          if (this.$route.name === 'rootHome') {
            this.$router.go()
          } else {
            this.$router.push({ name: 'rootHome' }).catch(err => {
              if (err) {
                this.$router.go()
              }
            })
          }

          this.emitClose()
        })
        .catch(() => {
          this.$q.notify({
            icon: 'warning',
            color: 'negative',
            message: 'Something went wrong!'
          })

          this.logIn = {}
        })
    },
    emitClose: function () {
      this.$emit('close')
    }
  }
}
</script>

<style lang="stylus">

</style>
