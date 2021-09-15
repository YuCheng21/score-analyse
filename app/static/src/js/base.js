$(document).ready(function () {
    // console.log('ready')

})

/**
 * sweetAlert
 */
function errorDialog(category, message) {
    if (category === 'error') {
        Swal.fire(
            '錯誤',
            message,
            'error'
        )
    } else if (category === 'success') {
        Swal.fire(
            '成功',
            message,
            'success'
        )
    } else if (category === 'success-toast') {
        const Toast = Swal.mixin({
            toast: true,
            position: 'bottom-end',
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: true,
            didOpen: (toast) => {
                toast.addEventListener('mouseenter', Swal.stopTimer)
                toast.addEventListener('mouseleave', Swal.resumeTimer)
            }
        })

        Toast.fire({
            icon: 'success',
            title: message
        })
    }
}