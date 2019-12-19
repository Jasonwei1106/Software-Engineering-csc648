<template>
  <div
    class="q-pa-md"
    style="margin: 1em auto;"
  >
    <q-form @submit.prevent.stop="onSubmit">
      <div align="center">
        <div class="q-gutter-md" style="width: 35vw; min-width: 270px;">
          <q-input
            dense outlined required
            bg-color="white" type="text"
            placeholder="Username"
            v-model="logIn.username"
          />

          <q-input
            dense outlined required
            bg-color="white" type="email"
            placeholder="Email"
            v-model="logIn.email"
          />

          <q-input
            dense outlined required
            bg-color="white" type="password"
            placeholder="Password"
            v-model="logIn.password"
          />

          <q-input
            dense outlined
            bg-color="white" type ="password"
            placeholder="Confirm Password"
            v-model="logIn.conpassword"
          />
        </div>

        <div
          class="q-my-md row" align="center"
          style="width: 30vw; min-width: 270px;"
        >
          By clicking "Sign Up" you agree to our Terms and to our Privacy Statment.
        </div>

        <div align="center" >
          <q-btn
            no-caps
            type="submit" color="primary" label="Sign Up"
            style="width: 15%; min-width: 150px;"
          />
        </div>
      </div>
    </q-form>
  </div>
</template>

<script>
import axios from 'axios'
// import md5 from 'md5'

export default {
  data () {
    return {
      logIn: {}
    }
  },
  methods: {
    onSubmit: function () {
      if (!(/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(this.logIn.email))) {
        this.$q.notify({
          message: 'Your email is not in the vaild format!'
        })
      } else if (this.logIn.conpassword !== this.logIn.password) {
        this.$q.notify({
          message: 'Your confirm password doesn\'t match'
        })
      } else {
        axios.post('http://54.67.109.241:5000/api/user/create', {
          email_address: this.logIn.email,
          username: this.logIn.username,
          password: this.logIn.password
        })
          .then(res => {
            this.$q.notify({
              icon: 'done',
              color: 'positive',
              message: 'Submitted'
            })
            this.logIn = {}
            this.$router.push({ name: 'rootHome' })
          })
          .catch(() => {
            this.$q.notify({
              icon: 'warning',
              color: 'negative',
              message: 'Something went wrong!'
            })
          })
      }
    }
  }
}
</script>
