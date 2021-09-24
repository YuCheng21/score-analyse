$(document).ready(function () {
    // console.log('ready')

})

/**
 * Theme Color
 */
const style = getComputedStyle(document.body);
const theme = {};
theme.primary = style.getPropertyValue('--bs-primary');
theme.secondary = style.getPropertyValue('--bs-secondary');
theme.success = style.getPropertyValue('--bs-success');
theme.info = style.getPropertyValue('--bs-info');
theme.warning = style.getPropertyValue('--bs-warning');
theme.danger = style.getPropertyValue('--bs-danger');
theme.light = style.getPropertyValue('--bs-light');
theme.dark = style.getPropertyValue('--bs-dark');

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