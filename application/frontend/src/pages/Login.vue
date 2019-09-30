<template>
  <div class="q-pa-md">
    <strong>Login</strong>
    <hr>
    <q-form @submit="onSubmit">
      <div class="q-pa-md">
        <div class="row">
          <q-input
            type="text"
            placeholder="username here plz..."
            prefix="Username:"
            v-model="logIn.name"
          >
            <template v-slot:prepend>
              <q-icon name="mail" />
            </template>
          </q-input>
        </div>
        <div class="row">
          <q-input
            type="password"
            placeholder="password..."
            prefix="Password:"
            v-model="logIn.password"
          >
            <template v-slot:prepend>
              <q-icon name="vpn_key" />
            </template>
          </q-input>
        </div>
      </div>

      <div class="row q-gutter-sm">
        <q-btn no-caps type="submit" >Log In</q-btn>
        <q-btn no-caps @click="closeLogIn" >Cancle</q-btn>
      </div>
    </q-form>
  </div>
</template>

<script>
export default {
  data () {
    return {
      logIn: {}
    }
  },
  methods: {
    onSubmit: function () {
      console.log('gigy')

      this.logIn = {}
    },
    closeLogIn: function () {
      this.$emit('close')
    }
  }
}
</script>

<style>

</style>
