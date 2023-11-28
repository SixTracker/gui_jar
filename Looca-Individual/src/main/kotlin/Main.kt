import javax.swing.JOptionPane
import javax.swing.JOptionPane.*

fun main() {
    val py = ApiPython
    val pyServer = ApiPythonSqlServer
    val login = Usuario()
    login.iniciar()

    login.email = showInputDialog("Digite o seu email:").toString()
    login.senha = showInputDialog("Digite a sua senha:").toString()

        if (login.validarLogin(login)) {
            showMessageDialog(null, login.comprimentar(login))
            val fkEmpresa = login.verificarEmpresa(login)
            val listaDeServidor = fkEmpresa?.let { login.mostrarServidor(it) }
            showConfirmDialog(null, "O monitoramento irá inicializar agora!")
            val idServidor =
                showInputDialog("Digite o ID do servidor que você deseja monitorar:\n\r $listaDeServidor")
                    .toInt()

            val listaDeComponente = login.mostrarComponentes(idServidor)
            val fkComponenteCPU =
                showInputDialog("Digite o ID do componente  de cpu que você deseja monitorar:\n\r $listaDeComponente")
                    .toInt()
            val fkComponenteRAM =
                showInputDialog("Digite o ID do componente de ram que você deseja monitorar:\n\r $listaDeComponente")
                    .toInt()


            pyServer.chamarApiPython(idServidor, fkComponenteCPU, fkComponenteRAM)
        }

}
