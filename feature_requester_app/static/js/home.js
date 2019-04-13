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

    self.all_feature_requests = ko.observableArray([]);
    self.feature_request = ko.observableArray();
    self.errors = ko.observableArray();
    
    // Fetch all feature requests from database using our API
    $.getJSON("/api/feature_requests/", (data) => {
        var feature_requests_from_api = $.map(
            data['feature_requests'], (item) => {
                return new FeatureRequestModel(item);
            });
        self.all_feature_requests(feature_requests_from_api);
    });

    self.clients = ko.observableArray([]);

    // Fetch all clients from database using our API
    $.getJSON("/api/clients/", (data) => {
        var clients_from_api = $.map(
            data['clients'], (item) => {
                return new ClientModel(item);
            });
        self.clients(clients_from_api);
    });

    self.product_areas = ko.observableArray([]);

    // Fetch all product areas from database using our API
    $.getJSON("/api/product_areas/", (data) => {
        var product_areas_from_api = $.map(
            data['product_areas'], (item) => {
                return new ProductAreaModel(item);
            });
        self.product_areas(product_areas_from_api);
    });

    // AJAX method to add a new feature request using a modal form
    self.addFeatureRequest = () => {
        var data = $("form#feature_request_form")
            .serializeArray()
            .map(function(x) {
                this[x.name] = x.value;
                return this;
            }.bind({}))[0];

        $.ajax({
            contentType: "application/json;",
            dataType: "json",
            method: "POST",
            url: "/api/feature_requests/add/",
            data: JSON.stringify(data),
            success: (data) => {
                $("#feature_request_modal").modal("hide");
                document.getElementById("feature_request_form").reset();
                self.all_feature_requests.push(
                    new FeatureRequestModel(ko.toJS(data['data'][0]))
                );
                alert(data['message']);
            },
            error: (errors) => {
                self.errors(errors.responseJSON.errors);
                alert(errors['message']);
            }
        });
    };
}

var featureRequestVM = new FeatureRequestViewModel();
ko.applyBindings(featureRequestVM); // Activate KnockoutJS bindings