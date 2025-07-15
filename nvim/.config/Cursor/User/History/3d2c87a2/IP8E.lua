format_on_save = function(bufnr)
  -- Disable "format_on_save lsp_fallback" for languages that don't
  -- have a well standardized coding style. You can add additional
  -- languages here or re-enable it for the disabled ones.
  local disable_filetypes = { c = true, cpp = true, templ = true }
  local lsp_format_opt
  if disable_filetypes[vim.bo[bufnr].filetype] then
    lsp_format_opt = 'never'
  else
    lsp_format_opt = 'fallback'
  end
  return {
    timeout_ms = 500,
    lsp_format = lsp_format_opt,
  }
end,

-- set golang tab spacing to 4 spaces. seems 8 is the annoying default
vim.api.nvim_create_autocmd("FileType", {
  pattern = "go",
  callback = function()
    vim.opt_local.tabstop = 4
    vim.opt_local.shiftwidth = 4
    vim.opt_local.softtabstop = 4
    vim.opt_local.expandtab = false  -- Go uses real tabs
  end,
}),

-- Disable auto-formatting and text wrapping for .templ files
vim.api.nvim_create_autocmd({"BufRead", "BufNewFile"}, {
  pattern = "*.templ",
  callback = function()
    vim.opt_local.textwidth = 0
    vim.opt_local.wrapmargin = 0
    vim.opt_local.formatoptions:remove("t")
    vim.opt_local.formatoptions:remove("c")
    vim.opt_local.formatoptions:remove("a")
    vim.bo.filetype = "templ"
  end,
}), 