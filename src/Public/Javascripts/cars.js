
const handleDelete = (car_id) => {
    if (confirm('Delete this car?') == true) {
        fetch(`/cars/${car_id}`, {
            method: "POST",
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        })
        window.location.replace("/cars")
    }
}