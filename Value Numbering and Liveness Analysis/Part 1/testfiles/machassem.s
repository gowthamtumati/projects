	.text
	.file	"test.c"
	.globl	gcd                     # -- Begin function gcd
	.p2align	4, 0x90
	.type	gcd,@function
gcd:                                    # @gcd
	.cfi_startproc
# %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	movl	%edi, -16(%rbp)
	movl	%esi, -12(%rbp)
	movl	$1, -8(%rbp)
	movl	$2, -4(%rbp)
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	xorl	%eax, %eax
	movl	-4(%rbp), %ecx
	cmpl	-16(%rbp), %ecx
	jg	.LBB0_3
# %bb.2:                                #   in Loop: Header=BB0_1 Depth=1
	movl	-4(%rbp), %eax
	cmpl	-12(%rbp), %eax
	setle	%al
.LBB0_3:                                #   in Loop: Header=BB0_1 Depth=1
	testb	$1, %al
	jne	.LBB0_4
	jmp	.LBB0_9
.LBB0_4:                                #   in Loop: Header=BB0_1 Depth=1
	movl	-16(%rbp), %eax
	cltd
	idivl	-4(%rbp)
	cmpl	$0, %edx
	jne	.LBB0_7
# %bb.5:                                #   in Loop: Header=BB0_1 Depth=1
	movl	-12(%rbp), %eax
	cltd
	idivl	-4(%rbp)
	cmpl	$0, %edx
	jne	.LBB0_7
# %bb.6:                                #   in Loop: Header=BB0_1 Depth=1
	movl	-4(%rbp), %eax
	movl	%eax, -8(%rbp)
.LBB0_7:                                #   in Loop: Header=BB0_1 Depth=1
	jmp	.LBB0_8
.LBB0_8:                                #   in Loop: Header=BB0_1 Depth=1
	movl	-4(%rbp), %eax
	addl	$1, %eax
	movl	%eax, -4(%rbp)
	jmp	.LBB0_1
.LBB0_9:
	movl	-8(%rbp), %eax
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end0:
	.size	gcd, .Lfunc_end0-gcd
	.cfi_endproc
                                        # -- End function
	.globl	main                    # -- Begin function main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$16, %rsp
	.cfi_offset %rbx, -32
	.cfi_offset %r14, -24
	movl	$0, -28(%rbp)
	movl	$98, -24(%rbp)
	movl	$56, -20(%rbp)
	movl	-24(%rbp), %ebx
	movl	-20(%rbp), %r14d
	movl	-24(%rbp), %edi
	movl	-20(%rbp), %esi
	callq	gcd
	movabsq	$.L.str, %rdi
	movl	%ebx, %esi
	movl	%r14d, %edx
	movl	%eax, %ecx
	movb	$0, %al
	callq	printf
	xorl	%eax, %eax
	addq	$16, %rsp
	popq	%rbx
	popq	%r14
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc
                                        # -- End function
	.type	.L.str,@object          # @.str
	.section	.rodata.str1.1,"aMS",@progbits,1
.L.str:
	.asciz	"GCD of %d and %d is %d "
	.size	.L.str, 24


	.ident	"clang version 8.0.1 (tags/RELEASE_801/final)"
	.section	".note.GNU-stack","",@progbits
