// test google maps api

function initMap() {
    const locationPicker = document.getElementById('locationPicker')
    const map_options = {
        componentRestrictions: { country: 'ke' },
        fields: ['address_components', 'geometry', 'name', 'url'],
        strictBounds: false,
        types: ['address'],     // options: geocode, address, establishment
    }
    const autocomplete = new google.maps.places.Autocomplete(locationPicker, map_options)
    autocomplete.addListener('place_changed', () => {
        const place = autocomplete.getPlace()
        if (!place.geometry || !place.geometry.location) {
            // User entered the name of a Place that was not suggested and
            // pressed the Enter key, or the Place Details request failed.
            window.alert(`No details available for input: ' ${place.name}'`)
            return
        }

        const geocoder = new google.maps.Geocoder()
        const address = locationPicker.value

        geocoder.geocode({ 'address': address }, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                let latitude = results[0].geometry.location.lat()
                let longitude = results[0].geometry.location.lng()
                console.log(`latitude: ${latitude}`)
                console.log(`longitude: ${longitude}`)
            }
        })

        let address1 = ''
        let postcode = ''

        for (const component of place.address_components) {
            const componentType = component.types[0]

            switch (componentType) {
                case 'street_number': {
                    address1 = `${component.long_name} ${address1}`
                    break
                }
                case 'route': {
                    address1 += component.short_name
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
                case 'locality':
                    document.getElementById('city').value = component.long_name
                    break
                case 'administrative_area_level_1': {
                    document.getElementById('state').value = component.short_name
                    break
                }
                case 'country':
                    document.getElementById('country').value = component.long_name
                    break
            }
        }

        locationPicker.value = place.name
        document.getElementById('postcode').focus()

        console.log(place.icon)
        console.log(place.url)
        console.log('\n\n', place.address_components, '\n\n')
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