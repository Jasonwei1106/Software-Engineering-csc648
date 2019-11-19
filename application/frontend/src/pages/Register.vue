<template>
  <div
    class="q-pa-md"
    style="margin: 1em auto;"
  >
    <q-form @submit.prevent.stop="onSubmit">
      <div align="center">
        <div class="q-gutter-md" style="width: 35vw; min-width: 270px;">
          <q-input
            dense outlined
            bg-color="white"
            type="text"
            placeholder="Username"
            v-model="logIn.username"
            required
          />

          <q-input
            dense outlined
            bg-color="white"
            type="text"
            placeholder="Email"
            v-model="logIn.email"
            required
          />

          <q-input
            dense outlined
            bg-color="white"
            type="password"
            placeholder="Password"
            v-model="logIn.password"
            required
          />

          <q-input
            dense outlined
            bg-color="white"
            type ="password"
            placeholder="Confirm Password"
            v-model="logIn.conpassword"
          />
        </div>

        <div
          class="q-my-md row"
          align="left"
          style="width: 35vw; min-width: 270px;"
        >
          <q-checkbox
            v-model="customModel"
            color="primary"
            true-value="yes"
            false-value="no"
          >
            <span>
              Do you agree? {Please note: Terms and conditions will come...}
            </span>
          </q-checkbox>
        </div>

        <div align="center" >
          <q-btn
            no-caps
            type="submit"
            color="primary"
            label="Sign Up"
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
      customModel: 'no',
      logIn: {}
    }
  },
  methods: {
    onSubmit: function () {
      if (this.customModel !== 'yes') {
        this.$q.notify({
          color: 'negative',
          message: 'You need to accept the license and terms first'
        })
      } else if (this.logIn.conpassword !== this.logIn.password) {
        this.$q.notify({
          message: 'Your confirm password doesn\'t match'
        })
      } else {
        axios.post('http://54.153.68.76:5000/api/user/create', {
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
            this.customModel = 'no'
            this.logIn = {}
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
