import { ToastContainer as ToastifyContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

/**
 * Toast容器组件
 * 提供全局的toast提示功能
 */
export function ToastContainer() {
  return (
    <ToastifyContainer
      position="top-right"
      autoClose={3000}
      hideProgressBar={false}
      newestOnTop={false}
      closeOnClick
      rtl={false}
      pauseOnFocusLoss
      draggable
      pauseOnHover
      theme="light"
      toastClassName="!rounded-lg !shadow-lg !bg-white"
      bodyClassName="!text-gray-800"
      progressClassName="!bg-blue-600"
      closeButton={false}
    />
  )
}


