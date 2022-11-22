// test google maps api

const routeField = document.querySelector('#id_route')
const orgField = document.querySelector('#id_business_name')
const accTypeElm = document.querySelector('#id_account_type')

accTypeElm.addEventListener('change', () => {
    const accountType = selectedText(accTypeElm)
    const ffRoute = routeField.closest('.form-field')
    const ffOrg = orgField.closest('.form-field')

    if (accountType == 'Personal') {
        if (!ffOrg.classList.contains('d-none')) {
            ffOrg.classList.add('d-none')
        }
    }
    if (accountType == 'Organization') {
        if (ffOrg.classList.contains('d-none')) {
            ffOrg.classList.remove('d-none')
        }
    }
    if (ffRoute.classList.contains('d-none')) {
        ffRoute.classList.remove('d-none')
    }
})

/**
 * Returns select element selected text
 * @param {HTMLSelectElement} element select element
 */
function selectedText(element) {
    return element.options[element.selectedIndex].text
}


function initMap() {
    const autocompleteRoute = new google.maps.places.Autocomplete(routeField, {
        componentRestrictions: { country: 'ke' },
        fields: ['address_components', 'geometry', 'name', 'url'],
        strictBounds: false,
        types: ['address'],     // options: geocode, address, establishment
    })

    const autocompleteOrg = new google.maps.places.Autocomplete(orgField, {
        componentRestrictions: { country: 'ke' },
        fields: ['address_components', 'geometry', 'name', 'url'],
        strictBounds: false,
        types: ['establishment'],
    })

    const autos = []
    autos.push(autocompleteRoute)
    autos.push(autocompleteOrg)

    autos.forEach(element => {
        element.addListener('place_changed', () => {
            const place = element.getPlace()
            if (!place.geometry || !place.geometry.location) {
                // User entered the name of a Place that was not suggested and
                // pressed the Enter key, or the Place Details request failed.
                notifyError(`No details available for input: ' ${place.name}'`, false)
                return
            }

            let geo = null
            const geocoder = new google.maps.Geocoder()
            // const accountType = accTypeElm.options[accTypeElm.selectedIndex].text

            const routeChanged = () => autos.indexOf(element) == 0
            const orgChanged = () => autos.indexOf(element) == 1

            if (routeChanged()) {
                console.log('changed: route field!')
                geo = routeField.value
                routeField.value = place.name
            }
            if (orgChanged()) {
                console.log('changed: org name field!')
                geo = orgField.value
                orgField.value = place.name
            }

            geocoder.geocode({ 'address': geo }, function (results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    let latitude = results[0].geometry.location.lat()
                    let longitude = results[0].geometry.location.lng()
                    document.querySelector('#id_latitude').value = latitude
                    document.querySelector('#id_longitude').value = longitude
                }
            })

            let address1 = ''
            let postcode = ''

            for (const component of place.address_components) {
                const componentType = component.types[0]

                switch (componentType) {
                    // case 'street_number': {
                    //     address1 = `${component.long_name} ${address1}`
                    //     break
                    // }
                    case 'route': {
                        address1 = component.long_name
                        break
                    }
                    case 'postal_code': {
                        postcode = `${component.long_name}${postcode}`
                        break
                    }
                    case 'postal_code_suffix': {
                        postcode = `${postcode}-${component.long_name}`
                        break
                    }
                    case 'sublocality_level_1': {
                        document.querySelector('#id_neighbourhood').value = component.long_name
                        break
                    }
                    case 'locality': {
                        document.querySelector('#id_city').value = component.long_name
                        break
                    }
                    case 'administrative_area_level_1': {
                        document.querySelector('#id_county').value = component.short_name
                        break
                    }
                    case 'country':
                        document.querySelector('#id_country').value = component.long_name
                        break
                }
            }

            // addressField.value = place.name
            if (orgChanged()) {
                routeField.value = address1
            }
            document.querySelector('#id_postal_code').value = postcode

            if (routeChanged() && selectedText(accTypeElm) == 'Organization') {
                document.querySelector('#id_maps_url').value = document.querySelector('#id_maps_url').value
            } else {
                document.querySelector('#id_maps_url').value = place.url
            }
    
            console.log(place.url)
            console.log('\n\n', place.address_components, '\n\n')
        })
    })
}

/*
let autocomplete = null

$.getScript(`https://maps.googleapis.com/maps/api/js?key=${GOOGLE_API_KEY}&libraries=places`)
.done(function(script, textStatus) {
    google.maps.event.addDomListener(window, 'load', initAutoComplete)
})

function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        locationPicker,
        {
            types: ['address'],
            componentRestrictions: {'country': 'KE'}
        }
    )
    autocomplete.addListener('place_changed', onPlaceChanged)
}

function onPlaceChanged() {
    let place = autocomplete.getPlace()
    let geocoder = new google.maps.Geocoder()
    let address = locationPicker.value

    geocoder.geocode({'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            let latitude = results[0].geometry.location.lat()
            let longitude = results[0].geometry.location.lng()
            console.log(`latitude: ${latitude}`)
            console.log(`longitude: ${longitude}`)
        }
    })

    if(!place.geometry) {
        locationPicker.placeholder = 'Type correct address...'
    }
    else {
        console.log('\n\n', place.address_components, '\n\n')
        for (let i=0; i < place.address_components.length; i++) {
            for (let j=0; j < place.address_components[i].types.length; j++) {
                const val = place.address_components[i].long_name
                const valType = place.address_components[i].types[j]

                if (valType == 'street_number') console.log(`streetNumber: ${val}`)
                else if (valType == 'route') console.log(`route: ${val}`)
                else if (valType == 'postal_town') console.log(`postal_town: ${val}`)
                else if (valType == 'administrative_area_level2') console.log(`administrative_area_level2: ${val}`)
                else if (valType == 'country') console.log(`country: ${val}`)
                else if (valType == 'postal_code') console.log(`postal_code: ${val}`)
            }
        }
    }
}
*/

// editor js test
/*
const editorDOM = document.getElementById('editorjs')

const editor = new EditorJS({
    holder: 'editorjs',
    tools: {
        header: {
            class: Header,
            inlineToolbar: true
        },
        list: {
            class: List,
            inlineToolbar: true
        },
        linkTool: {
            class: LinkTool,
            config: {
                endpoint: `${SERVER}/static/media`, // Your backend endpoint for url data fetching,
            }
        },
        image: {
            class: ImageTool,
            // config: {
            //     endpoints: {
            //         byFile: `${SERVER}/static/media`, // Your backend file uploader endpoint
            //         byUrl: `${SERVER}/static/media`, // Your endpoint that provides uploading by Url
            //     }
            // }
        }
    },
    autofocus: true,
    placeholder: 'Start typing...',
    onReady: () => {
        console.log('Editor.js is ready to work!')
    },
    // onChange: () => {
    //     console.log('Editor content changing')
    //     editorFocus()
    // }
    // data: {}
})


new Array('click', 'mousedown', 'keydown').forEach(val => {
    document.addEventListener(val, (e) => {
        if (editorDOM.contains(e.target)) {
            editorDOM.classList.add('bs-focus')
        } else {
            editorDOM.classList.remove('bs-focus')
        }
    })
})

document.addEventListener('DOMContentLoaded', () => {
    editorDOM.classList.add('bs-focus')
})

document.getElementById('editorSaveBtn').addEventListener('click', () => {
    editor.save().then((outputData) => {
        console.log('Editor - output data: ', JSON.stringify(outputData))
    }).catch((error) => {
        console.log('Editor - saving failed: ', error)
    })
}) */