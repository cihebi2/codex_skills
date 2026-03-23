library(jsonlite)

ngplot_base_dir <- function(base_dir = NULL) {
  if (is.null(base_dir)) {
    normalizePath(dirname(sys.frame(1)$ofile %||% "catalog_loader.R"), winslash = "/", mustWork = FALSE)
  } else {
    normalizePath(base_dir, winslash = "/", mustWork = FALSE)
  }
}

`%||%` <- function(x, y) {
  if (is.null(x)) y else x
}

load_ngplot_catalog <- function(base_dir = NULL) {
  base <- ngplot_base_dir(base_dir)
  fromJSON(file.path(base, "catalog.json"), simplifyVector = FALSE)
}

list_ngplot_templates <- function(base_dir = NULL) {
  load_ngplot_catalog(base_dir)$templates
}

find_ngplot_templates <- function(keyword = NULL, category = NULL, has_python = NULL, has_r = NULL, base_dir = NULL) {
  items <- list_ngplot_templates(base_dir)
  keep <- rep(TRUE, length(items))

  if (!is.null(keyword) && nzchar(keyword)) {
    needle <- tolower(keyword)
    keep <- keep & vapply(items, function(item) {
      hay <- paste(item$name, item$id, item$category, item$categoryTrailText)
      grepl(needle, tolower(hay), fixed = TRUE)
    }, logical(1))
  }

  if (!is.null(category) && nzchar(category)) {
    keep <- keep & vapply(items, function(item) identical(item$category, category), logical(1))
  }

  if (!is.null(has_python)) {
    keep <- keep & vapply(items, function(item) identical(isTRUE(item$hasPython), has_python), logical(1))
  }

  if (!is.null(has_r)) {
    keep <- keep & vapply(items, function(item) identical(isTRUE(item$hasR), has_r), logical(1))
  }

  items[keep]
}

get_ngplot_template <- function(template_id, base_dir = NULL) {
  items <- list_ngplot_templates(base_dir)
  matched <- Filter(function(item) identical(item$id, template_id), items)
  if (length(matched) == 0) {
    stop(sprintf("Template not found: %s", template_id), call. = FALSE)
  }
  matched[[1]]
}

read_ngplot_bundle <- function(template_id, base_dir = NULL) {
  base <- ngplot_base_dir(base_dir)
  item <- get_ngplot_template(template_id, base)
  bundle <- item
  bundle$meta <- fromJSON(file.path(base, item$metaUrl), simplifyVector = FALSE)
  bundle$svg <- readChar(file.path(base, item$svgUrl), file.info(file.path(base, item$svgUrl))$size, useBytes = TRUE)
  bundle$data <- setNames(lapply(item$dataFiles, function(file_info) {
    readChar(file.path(base, file_info$url), file.info(file.path(base, file_info$url))$size, useBytes = TRUE)
  }), vapply(item$dataFiles, function(file_info) file_info$name, character(1)))
  if (!is.null(item$pythonUrl) && nzchar(item$pythonUrl)) {
    bundle$python_code <- readChar(file.path(base, item$pythonUrl), file.info(file.path(base, item$pythonUrl))$size, useBytes = TRUE)
  }
  if (!is.null(item$rUrl) && nzchar(item$rUrl)) {
    bundle$r_code <- readChar(file.path(base, item$rUrl), file.info(file.path(base, item$rUrl))$size, useBytes = TRUE)
  }
  bundle
}
