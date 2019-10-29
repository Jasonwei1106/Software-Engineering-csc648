<template>
  <div class="q-pa-md" style="width: 98%; margin: 1em auto;">
    <strong>Reset Password</strong>
    <q-stepper
      v-model="step"
      ref="stepper"
      vertical
      animated
      active-color="purple"
    >
      <q-step
        :name="1"
        prefix="1"
        title="Type your email"
      >
      <div>
        <strong>Email:</strong>
        <q-input
            dense filled
            type="text"
            placeholder="Email..."
            v-model="logIn.name"
            style ="max-width: 600px;"
          >
            <template v-slot:prepend>
              <q-icon name="mail" />
            </template>
          </q-input>
      </div>
      </q-step>

      <q-step
        :name="2"
        prefix="2"
        title="Type your code"
      >
      <div>
        <strong>Code:</strong>
        <q-input
            dense filled
            type="text"
            placeholder="confirm code..."
            v-model="logIn.code"
            style = "max-width: 200px;"
          >
            <template v-slot:prepend>
              <q-icon name="confirmation_number" />
            </template>
          </q-input>
      </div>
      </q-step>

      <q-step
        :name="3"
        prefix="3"
        title="Reset your new password"
      >
      <div>
        <strong>Password:</strong>
        <q-input
          dense filled
          type="password"
          placeholder="Password..."
          v-model="logIn.password"
          style ="max-width: 600px;"
        >
          <template v-slot:prepend>
              <q-icon name="vpn_key" />
            </template>
          </q-input>
        </div>
      </q-step>

      <q-step
        :name="4"
        prefix="4"
        title="Confirm your new password"
      >
        <div>
          <strong>Confirm Password:</strong>
          <q-input
            dense filled
            type ="password"
            placeholder="Password..."
            v-model="logIn.conpassword"
            style ="max-width: 600px;"
          >
            <template v-slot:prepend>
              <q-icon name="vpn_key" />
            </template>
          </q-input>
        </div>
      </q-step>

      <template v-slot:navigation>
        <q-stepper-navigation>
          <q-btn @click="onSubmit" color="deep-orange" :label="step === 4 ? 'Finish' : 'Continue'" />
          <q-btn v-if="step > 1" flat color="deep-orange" @click="$refs.stepper.previous()" label="Back" class="q-ml-sm" />
        </q-stepper-navigation>
      </template>
    </q-stepper>
  </div>
</template>

<script>
export default {
  data () {
    return {
      step: 1,
      logIn: {
        name: '',
        password: '',
        conpassword: ''
      },
      previousLog: {
        name: '',
        password: '',
        conpassword: ''
      }
    }
  },
  methods: {
    onSubmit: function () {
      if (this.step === 1 && this.logIn.name.length < 1) {
        this.$q.notify({
          message: 'Please enter something here'
        })
      } else if (this.step === 3 && this.logIn.password.length < 1) {
        this.$q.notify({
          message: 'Please enter password here'
        })
      } else if (this.step === 4 && this.logIn.password !== this.logIn.conpassword) {
        this.$q.notify({
          message: 'Your confirm password doesn\'t match'
        })
      } else {
        if (this.step !== 4) {
          this.step++
          this.previousLog = {
            ...this.logIn
          }
        }
      }
    },
    onBack: function () {
      this.logIn = {
        ...this.previousLog
      }
    }
  }
}
</script>
