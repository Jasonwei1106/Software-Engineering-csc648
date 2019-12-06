<template>
  <div class="q-mt-lg q-gutter-md">
    <q-btn
      color="negative"
      label="First"
      @click="copyURLtoClipboard"
    />

    <q-btn
      color="negative"
      label="Second"
      @click="copyToClipboard"
    />

    <q-btn
      color="negative"
      label="Third"
      @click="quasarCopy"
    />
  </div>
</template>

<script>
export default {
  data () {
    return {

    }
  },
  methods: {
    copyURLtoClipboard: function () {
      // https://stackoverflow.com/questions/6725890/location-host-vs-location-hostname-and-cross-browser-compatibility
      if (!window.location.origin) {
        window.location.origin = window.location.protocol + '//' + window.location.hostname + (window.location.port ? (':' + window.location.port) : '')
      }

      let routeData = window.location.origin + '/' + this.$router.resolve('', this.$route).href
      this.copyTextToClipboard(routeData)

      this.$q.notify({
        message: 'The URL has been copied to the clipboard.',
        position: 'top',
        timeout: 2000,
        color: 'info',
        textColor: 'white',
        actions: [
          {
            icon: 'close',
            color: 'white'
          }
        ]
      })
    },
    fallbackCopyTextToClipboard: function (entry) {
      // https://stackoverflow.com/questions/400212/how-do-i-copy-to-the-clipboard-in-javascript
      let textArea = document.createElement('textarea')
      textArea.value = entry
      document.body.prepend(textArea)
      // textArea.focus()
      textArea.select()

      try {
        document.execCommand('copy')
      } catch (err) {
        if (err) {
          // error
        }
      }

      document.body.removeChild(textArea)
    },
    copyTextToClipboard: function (entry) {
      // https://stackoverflow.com/questions/400212/how-do-i-copy-to-the-clipboard-in-javascript
      if (!navigator.clipboard) {
        this.fallbackCopyTextToClipboard(entry)
        // return
      } else {
        navigator.clipboard.writeText(entry).then(function () {
        }, function (err) {
          if (err) {
          }
        })
      }
    },
    copyToClipboard: function () {
      // https://stackoverflow.com/questions/400212/how-do-i-copy-to-the-clipboard-in-javascript
      if (!window.location.origin) {
        window.location.origin = window.location.protocol + '//' + window.location.hostname + (window.location.port ? (':' + window.location.port) : '')
      }

      let routeData = window.location.origin + '/' + this.$router.resolve('', this.$route).href

      window.prompt('Copy to clipboard: Ctrl+C, Enter', routeData)
    },
    quasarCopy: function () {
      if (!window.location.origin) {
        window.location.origin = window.location.protocol + '//' + window.location.hostname + (window.location.port ? (':' + window.location.port) : '')
      }

      let routeData = window.location.origin + '/' + this.$router.resolve('', this.$route).href

      this.$q.dialog({
        title: 'Confirm',
        message: routeData,
        cancel: true
      }).onOk(() => {
        // console.log('>>>> OK')
        this.copyURLtoClipboard()

        this.$q.notify({
          message: 'The URL has been copied to the clipboard.',
          position: 'top',
          timeout: 2000,
          color: 'info',
          textColor: 'white',
          actions: [
            {
              icon: 'close',
              color: 'white'
            }
          ]
        })
      }).onCancel(() => {
        // console.log('>>>> Cancel')
      }).onDismiss(() => {
        // console.log('I am triggered on both OK and Cancel')
      })
    }
  }
}
</script>

<style>

</style>
