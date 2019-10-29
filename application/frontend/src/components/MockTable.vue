<template>
  <div class="q-pa-md">
    <q-table
      title="DIYup Tutorials"
      row-key="title"
      :data="curData"
      :columns="columns"
      :filter="option"
      :pagination.sync="pagination"
    >
      <!-- <template v-slot:top-right>
          <q-toolbar>
            <q-btn
              round dense flat
              class="q-mr-xs" icon="menu"
            >
              <q-menu dense>
                <q-list
                  v-for="(keyword, index) in popkeywords"
                  :key="index"
                  style="min-width: 100px;"
                >
                  <q-item clickable v-close-popup dense>
                    <q-item-section
                      v-if="option === keyword.value"
                      class="text-primary"
                      @click="option = keyword.value"
                    >
                      {{ keyword.label }}
                    </q-item-section>
                    <q-item-section v-else @click="option = keyword.value">
                      {{ keyword.label }}
                    </q-item-section>
                  </q-item>
                  <q-separator />
                </q-list>
              </q-menu>
            </q-btn>

            <q-space />

            <q-input
              dense
              debounce="300"
              color="primary" placeholder="keyword search"
              style="min-width: 20vw;"
              v-model="filter"
              @input="test"
            >
              <template v-slot:append>
                <q-icon v-if="filter === ''" name="search" />
                <q-icon v-else name="clear" class="cursor-pointer" @click="filter = ''; test()" />
              </template>
            </q-input>
          </q-toolbar>
        </template> -->

      <template v-slot:body-cell-title="props">
        <q-td :props="props">
          <div>
            <q-badge color="purple" :label="props.value" />
          </div>
          <!-- <div class="my-table-details">
            {{ props.row.details }}
          </div> -->
        </q-td>
      </template>
    </q-table>
    <!-- {{ data }} -->
  </div>
</template>

<script>
import axios from 'axios'

export default {
  // props: {
  //   filter: String
  // },
  created () {
    this.fetchData()
  },
  data () {
    return {
      popkeywords: [
        { label: 'Electronics', value: 'electronics' },
        { label: 'Coding', value: 'coding' },
        { label: 'Robotics', value: 'robotics' },
        { label: 'Testing', value: 'testing' },
        { label: 'All', value: '' }
      ],
      filter: '',
      option: '',
      columns: [
        {
          name: 'title',
          label: 'Title',
          required: true,
          align: 'left',
          field: row => row.title,
          format: val => `${val}`,
          sortable: true
        },
        {
          name: 'author_difficulty',
          label: `Creator's Difficulty`,
          required: true,
          align: 'left',
          field: row => row.author_difficulty,
          format: val => `${val}`,
          sortable: true
        },
        {
          name: 'category',
          label: `Category`,
          required: true,
          align: 'left',
          field: row => row.category,
          format: val => `${val}`,
          sortable: true
        }
      ],
      data: [],
      curData: [],
      pagination: {
        rowsPerPage: 10,
        sortBy: 'name',
        descending: false
      }
    }
  },
  methods: {
    test: function () {
      if (this.filter) {
        this.curData = this.data.filter(v => v.title.toLowerCase().includes(this.filter.toLowerCase()))
      } else {
        this.curData = this.data
      }
    },
    fetchData: function () {
      axios.get('http://54.153.68.76:5000/api/tutorial/get')
        .then(res => {
          this.data = res.data.tutorials
          this.data.forEach(element => {
            this.curData.push(element)
          })
        })
    }
  }
}
</script>

<style lang="stylus">
.my-table-details {
  font-size: 0.85em;
  font-style: italic;
  max-width: 200px;
  white-space: normal;
  color: #555;
  margin-top: 4px;
}
</style>
