# Dotfiles

Configuración personal de mi sistema **Arch Linux** con KDE Plasma.

## Instalación

```bash
git clone https://github.com/Facu-Glo/Dotfiles.git ~/Dotfiles
cd ~/Dotfiles
./install.sh
```

El script `install.sh` se encarga de todo:

1. **Bootstrap** — configura pacman, actualiza el sistema, instala paquetes (pacman + AUR) y habilita servicios (bluetooth, sddm, tlp)
2. **Repos externos** — clona configuración de Neovim y fondos de pantalla
3. **GRUB** — copia el tema Vimix y genera `grub.cfg`
4. **findgit** — instala el script `findgit` en `~/.local/bin/`
5. **Stow** — vincula todas las configuraciones con GNU Stow

> ⚠️ Ejecutalo en un sistema Arch recién instalado o usá los componentes que te sirvan por separado.

## Estructura

```
Dotfiles/
├── bootstrap.sh          # Paquetes, servicios, config inicial
├── install.sh            # Entry point que orquesta todo
├── packages/
│   ├── pacman.txt        # Paquetes oficiales
│   └── aur.txt           # Paquetes de AUR
├── external/
│   └── repos.txt         # Repos externos a clonar
├── system/
│   ├── grub/             # Tema Vimix + /etc/default/grub
│   └── findgit/          # Script findgit
└── stow/                 # Configs por app (linkeadas con stow)
    ├── fastfetch/
    ├── findgit/
    ├── kitty/
    ├── lazygit/
    ├── opencode/
    ├── starship/
    ├── yazi/
    └── zsh/
```

## Lo que incluye

| App           | Qué configura                                                                       |
| ------------- | ----------------------------------------------------------------------------------- |
| **Kitty**     | Terminal con Tokyo Night, tab bar personalizada, smart resize                       |
| **ZSH**       | zsh-autosuggestions, zsh-syntax-highlighting, history substring search, zoxide, fzf |
| **Starship**  | Prompt rápido e informativo                                                         |
| **Neovim**    | Configuración completa (repo separado)                                              |
| **Yazi**      | File explorer con tema Tokyo, starship, full-border                                 |
| **LazyGit**   | TUI para git                                                                        |
| **FastFetch** | Info del sistema al abrir la terminal                                               |
| **opencode**   | Configuración del asistente AI opencode con tema Tokyo Night y agentes                            |
| **GRUB**      | Tema Vimix                                                                          |

## Servicios habilitados

- `bluetooth.service`
- `sddm.service`
- `tlp.service`
