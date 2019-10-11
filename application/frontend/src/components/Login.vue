<template>
  <div class="q-pa-md" style="width: 23vw; min-width: 270px;" >
    <strong>Login</strong>
    <hr>
    <q-form @submit="onSubmit">
      <div class="q-pa-md" >

        <div>
          <strong>Email:</strong>
          <q-input
            dense filled
            type="text"
            placeholder="Email..."
            v-model="logIn.name"
          >
            <template v-slot:prepend>
              <q-icon name="mail" />
            </template>
          </q-input>
        </div>

        <div>
          <strong>Password:</strong>
          <q-input
            dense filled
            type="password"
            placeholder="Password..."
            v-model="logIn.password"
          >
            <template v-slot:prepend>
              <q-icon name="vpn_key" />
            </template>
          </q-input>
        </div>
      </div>

      <div class="q-pa-xs">
        <div align="center" class="q-mb-md">
          <q-btn no-caps class="full-width" type="submit" color="primary" label="Log In" />
          <br>
        </div>

        <router-link to="/forgot">
          Forgot your email or password?
        </router-link>
        <br>

        <span>
          Don't have an acoount? <router-link to="/register">Sign up here!</router-link>
        </span>
      </div>
    </q-form>
  </div>
</template>

<script>
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
      this.logIn = {}
    }
  }
}
</script>

<style lang="stylus">

</style>
