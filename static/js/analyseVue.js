let spinner = '<div class="uk-flex uk-flex-center uk-flex-middle uk-height-large">' +
    '<span uk-spinner="ratio: 4.5"></span>' +
    '</div>';

let analyseVue = new Vue({
    el: "#app",
    delimiters: ['[[', ']]'],
    data: getInitialData(),
    methods: {
        changePreview(event) {
            let reader = new FileReader();
            this.file = event.target.files[0];
            reader.readAsDataURL(this.file);
            reader.onload = function () {
                this.src = reader.result;
            }.bind(this);
        },
        submit(event) {
            let formData = new FormData();
            formData.append("file", this.file);
            let headers = {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            };
            this.result = spinner;
            console.log(this.result);
            axios.post(
                this.url,
                formData,
                headers
            ).then(function (response) {
                    console.log(response);
                    this.result = response.data;
                }.bind(this)
            ).catch(function (error) {
                    console.log(error);
                    this.result = "An error occurred while retrieving data from server";
                }.bind(this)
            )
        }
    }
});