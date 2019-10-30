<template>
  <div class="">
      <!-- title="DIYup Tutorials" -->
    <q-table
      flat
      row-key="title"
      :data="curData"
      :columns="columns"
      :filter="option.value"
      :pagination.sync="pagination"
    >
      <template v-slot:top-right>
          <q-toolbar>
            <q-select
              outlined dense
              class="q-mr-xs col-4" label="Filter"
              bg-color="white" color="black"
              v-model="option"
              style="width: 150px;"
              :options="categories"
            />
          </q-toolbar>
        </template>

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
  watch: {
    $route: 'titleQueryFilter'
  },
  created () {
    this.fetchData()
    this.filter = this.$route.query.title || ''
  },
  data () {
    return {
      filter: '',
      categories: [
        { label: 'Electronics', value: 'electronics' },
        { label: 'Coding', value: 'coding' },
        { label: 'Robotics', value: 'robotics' },
        { label: 'Cooking', value: 'cooking' },
        { label: 'Crafts', value: 'crafts' },
        { label: 'Home & Decor', value: 'homeDecor' },
        { label: 'Testing', value: 'testing' },
        { label: 'All', value: '' }
      ],
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
    titleQueryFilter: function () {
      this.filter = this.$route.query.title
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
