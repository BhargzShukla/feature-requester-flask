/*
Feature Request object model
*/
class FeatureRequestModel {
    constructor(data) {
        var self = this;

        self.id = ko.observable(data.id);
        self.title = ko.observable(data.title);
        self.description = ko.observable(data.description);
        self.client_id = ko.observable(data.client_id);
        self.client = ko.observable(data.client);
        self.client_priority = ko.observable(data.client_priority);
        self.product_area_id = ko.observable(data.product_area_id);
        self.product_area = ko.observable(data.product_area);
        self.target_date = ko.observable(data.target_date);
        self.created_on = ko.observable(data.created_on);
        self.updated_on = ko.observable(data.updated_on);
    }
}

/*
Client object model
*/
class ClientModel {
    constructor(data) {
        var self = this;

        self.id = ko.observable(data.id);
        self.name = ko.observable(data.name);
    }
}

/*
Product Area object model
*/
class ProductAreaModel {
    constructor(data) {
        var self = this;

        self.id = ko.observable(data.id);
        self.name = ko.observable(data.name);
    }
}

/*
ViewModel that contains all page logic
*/
function FeatureRequestViewModel() {
    var self = this;

    self.allFeatureRequests = ko.observableArray([]);
    self.featureRequest = ko.observableArray();
    self.errors = ko.observableArray();

    self.clients = ko.observableArray([]);
    self.productAreas = ko.observableArray([]);

    // Fetch all feature requests from database using our API
    self.getFeatureRequests = () => {
        $.getJSON("/api/feature_requests/", (data) => {
            var featureRequestsFromApi = $.map(
                data['feature_requests'], (item) => {
                    return new FeatureRequestModel(item);
                });
            self.allFeatureRequests(featureRequestsFromApi);
        });
    };
    self.getFeatureRequests();

    // Fetch all clients from database using our API
    self.getClients = () => {
        $.getJSON("/api/clients/", (data) => {
            var clientsFromApi = $.map(
                data['clients'], (item) => {
                    return new ClientModel(item);
                });
            self.clients(clientsFromApi);
        });
    }
    self.getClients();

    // Fetch all product areas from database using our API
    self.getProductAreas = () => {
        $.getJSON("/api/product_areas/", (data) => {
            var productAreasFromApi = $.map(
                data['product_areas'], (item) => {
                    return new ProductAreaModel(item);
                });
            self.productAreas(productAreasFromApi);
        });
    }
    self.getProductAreas();

    // AJAX method to add a new feature request using a modal form
    self.addFeatureRequest = () => {
        // self.getFeatureRequests();
        var data = $("form#feature_request_form")
            .serializeArray()
            .map(function (x) {
                this[x.name] = x.value;
                return this;
            }.bind({}))[0];

        $.ajax({
                contentType: "application/json;",
                dataType: "json",
                method: "POST",
                url: "/api/feature_requests/add/",
                data: JSON.stringify(data)
            })
            .done(function (data) {
                $("#feature_request_modal").modal("hide");
                self.allFeatureRequests.push(
                    new FeatureRequestModel(ko.toJS(data['data'][0]))
                );
                document.getElementById("feature_request_form").reset();
                self.getFeatureRequests();
                alert(data['message']);
            })
            .fail(function (jqxhr, textStatus, errorThrown) {
                var responseBody = jqxhr.responseText;
                console.log(responseBody);
                alert(responseBody);
            });
    };
}

ko.applyBindings(new FeatureRequestViewModel()); // Activate KnockoutJS bindings