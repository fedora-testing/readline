# Makefile for source rpm: readline
# $Id$
NAME := readline
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
